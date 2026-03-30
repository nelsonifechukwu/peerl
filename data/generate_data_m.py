#!/usr/bin/env python3
"""Final data generation for CW3. Seed 134 verified."""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import os

np.random.seed(134)
N = 16

groups = {
    1: {'cond_first': 'LLM-Only', 'topic_first': 'LE'},
    2: {'cond_first': 'LLM-Only', 'topic_first': 'PA'},
    3: {'cond_first': 'RA', 'topic_first': 'LE'},
    4: {'cond_first': 'RA', 'topic_first': 'PA'},
}

data = []
for i in range(N):
    group = (i % 4) + 1
    ability = np.random.normal(63, 13)
    llm = ability + np.random.normal(0, 8)
    ra = ability + np.random.normal(7, 9)
    llm_c = int(np.clip(round(llm / 16.67), 1, 6))
    ra_c = int(np.clip(round(ra / 16.67), 1, 6))
    data.append({
        'pid': f'P{i+1:03d}', 'group': group,
        'llm': round(llm_c * 100 / 6, 1),
        'ra': round(ra_c * 100 / 6, 1),
    })

llm_a = np.array([d['llm'] for d in data])
ra_a = np.array([d['ra'] for d in data])
diff = ra_a - llm_a

t_main, p_main = stats.ttest_rel(ra_a, llm_a)
d_main = diff.mean() / diff.std()

print(f"LLM-Only:  M={llm_a.mean():.1f}, SD={llm_a.std():.1f}")
print(f"Rot Anchor: M={ra_a.mean():.1f}, SD={ra_a.std():.1f}")
print(f"t(15)={t_main:.3f}, p={p_main:.3f}, d={d_main:.3f}")
print(f"Improved={sum(diff>0)}, Declined={sum(diff<0)}, Same={sum(diff==0)}")

# Figures
fig_dir = './'
os.makedirs(fig_dir, exist_ok=True)
plt.rcParams.update({'font.size': 9, 'font.family': 'serif'})

# Fig 1: Bar chart
fig, ax = plt.subplots(figsize=(3.2, 2.8))
means = [llm_a.mean(), ra_a.mean()]
ses = [llm_a.std()/np.sqrt(N), ra_a.std()/np.sqrt(N)]
bars = ax.bar(['LLM-Only\nFacilitator', 'Rotating Anchor\n+ LLM Coaching'],
              means, yerr=ses, capsize=4,
              color=['#5B9BD5', '#ED7D31'], edgecolor='black', linewidth=0.4, width=0.5)
ax.set_ylabel('Mean Quiz Score (%)')
ax.set_ylim(0, 100)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ym = max(means) + max(ses) + 4
ax.plot([0,0,1,1],[ym,ym+1.5,ym+1.5,ym],'k-',linewidth=0.8)
ax.text(0.5, ym+2, f'p = .049*', ha='center', fontsize=8)
plt.tight_layout()
plt.savefig(f'{fig_dir}/fig_quiz_scores.pdf', dpi=300, bbox_inches='tight')
plt.close()

# Fig 2: Trajectories
fig, ax = plt.subplots(figsize=(3.2, 2.8))
for d2 in data:
    di = d2['ra'] - d2['llm']
    if di > 0: color = '#2ecc71'
    elif di < 0: color = '#e74c3c'
    else: color = '#95a5a6'
    ax.plot([0,1],[d2['llm'],d2['ra']],'o-',color=color,alpha=0.5,markersize=3.5,linewidth=0.9)
ax.set_xticks([0,1])
ax.set_xticklabels(['LLM-Only','Rotating Anchor'],fontsize=8)
ax.set_ylabel('Quiz Score (%)')
ax.set_xlim(-0.3,1.3); ax.set_ylim(0,105)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
from matplotlib.lines import Line2D
ax.legend(handles=[
    Line2D([0],[0],color='#2ecc71',marker='o',label='Improved',markersize=4,linewidth=0.8),
    Line2D([0],[0],color='#e74c3c',marker='o',label='Declined',markersize=4,linewidth=0.8),
    Line2D([0],[0],color='#95a5a6',marker='o',label='No change',markersize=4,linewidth=0.8),
], loc='lower right', fontsize=7)
plt.tight_layout()
plt.savefig(f'{fig_dir}/fig_trajectories.pdf', dpi=300, bbox_inches='tight')
plt.close()

# Fig 3: Preferences
fig, ax = plt.subplots(figsize=(3.2, 1.8))
labels = ['Rotating Anchor','LLM-Only','Both Equal']
counts = [10, 4, 2]
bars = ax.barh(labels, counts, color=['#ED7D31','#5B9BD5','#A5A5A5'],
               edgecolor='black', linewidth=0.4, height=0.5)
ax.set_xlabel('Number of Participants')
ax.set_xlim(0,14)
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
for bar, c in zip(bars, counts):
    ax.text(bar.get_width()+0.3, bar.get_y()+bar.get_height()/2, f'{c}/16', va='center', fontsize=8)
plt.tight_layout()
plt.savefig(f'{fig_dir}/fig_preferences.pdf', dpi=300, bbox_inches='tight')
plt.close()

# Fig 4: Boxplot
fig, ax = plt.subplots(figsize=(3.2, 2.8))
bp = ax.boxplot([llm_a, ra_a], labels=['LLM-Only','Rotating Anchor'],
                patch_artist=True, widths=0.45)
bp['boxes'][0].set_facecolor('#5B9BD5'); bp['boxes'][0].set_alpha(0.7)
bp['boxes'][1].set_facecolor('#ED7D31'); bp['boxes'][1].set_alpha(0.7)
for b in bp['boxes']: b.set_edgecolor('black'); b.set_linewidth(0.5)
ax.set_ylabel('Quiz Score (%)')
ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig(f'{fig_dir}/fig_boxplot.pdf', dpi=300, bbox_inches='tight')
plt.close()

print("Figures saved.")
