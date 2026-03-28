"""
Data Analysis Script for CW3 Results Section
Run this after collecting all N=16 participants' data

Instructions:
1. Export data: curl http://localhost:8000/api/data/export > study_data.json
2. Run this script: python analyze_data.py
3. Copy results into CW3 report
"""

import json
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# Set styling for publication-quality figures
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

def load_data(filename='study_data.json'):
    """Load exported study data"""
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def calculate_quiz_scores(data):
    """Calculate quiz scores per participant per condition"""
    
    # Extract quiz responses
    quiz_responses = pd.DataFrame([
        {
            'participant_id': session['participant_id'],
            'module_number': session['module_number'],
            'condition': session['condition'],
            'topic': session['topic'],
            'question_number': response['question_number'],
            'is_correct': response['is_correct']
        }
        for session in data['sessions']
        for response in data['quiz_responses']
        if response['session_id'] == session['id']
    ])
    
    # Calculate percentage scores per session
    scores = quiz_responses.groupby([
        'participant_id', 'module_number', 'condition', 'topic'
    ])['is_correct'].mean() * 100
    
    scores_df = scores.reset_index()
    scores_df.columns = ['participant_id', 'module_number', 'condition', 'topic', 'score_percentage']
    
    return scores_df

def primary_analysis(scores_df):
    """Paired t-test: LLM-Only vs Rotating Anchor"""
    
    print("="*60)
    print("PRIMARY ANALYSIS: Paired t-test")
    print("="*60)
    
    # Reshape for paired comparison
    pivot = scores_df.pivot_table(
        index='participant_id',
        columns='condition',
        values='score_percentage'
    )
    
    llm_only_scores = pivot['llm_only'].dropna()
    rotating_anchor_scores = pivot['rotating_anchor'].dropna()
    
    # Descriptive statistics
    print(f"\nDescriptive Statistics:")
    print(f"  LLM-Only:")
    print(f"    Mean: {llm_only_scores.mean():.2f}%")
    print(f"    SD: {llm_only_scores.std():.2f}%")
    print(f"    Range: {llm_only_scores.min():.2f}% - {llm_only_scores.max():.2f}%")
    print(f"\n  Rotating Anchor:")
    print(f"    Mean: {rotating_anchor_scores.mean():.2f}%")
    print(f"    SD: {rotating_anchor_scores.std():.2f}%")
    print(f"    Range: {rotating_anchor_scores.min():.2f}% - {rotating_anchor_scores.max():.2f}%")
    
    # Paired t-test
    t_stat, p_value = stats.ttest_rel(llm_only_scores, rotating_anchor_scores)
    
    # Effect size (Cohen's d for paired samples)
    mean_diff = rotating_anchor_scores.mean() - llm_only_scores.mean()
    std_diff = (rotating_anchor_scores - llm_only_scores).std()
    cohens_d = mean_diff / std_diff
    
    print(f"\nInferential Statistics:")
    print(f"  t({len(llm_only_scores)-1}) = {t_stat:.3f}")
    print(f"  p = {p_value:.4f} {'*' if p_value < 0.05 else '(ns)'}")
    print(f"  Cohen's d = {cohens_d:.3f}")
    
    # Interpretation
    if abs(cohens_d) < 0.2:
        effect_interpretation = "negligible"
    elif abs(cohens_d) < 0.5:
        effect_interpretation = "small"
    elif abs(cohens_d) < 0.8:
        effect_interpretation = "medium"
    else:
        effect_interpretation = "large"
    
    print(f"  Effect size interpretation: {effect_interpretation}")
    
    # Check assumptions
    print(f"\nAssumption Checks:")
    
    # Normality test (Shapiro-Wilk)
    _, p_norm_llm = stats.shapiro(llm_only_scores)
    _, p_norm_ra = stats.shapiro(rotating_anchor_scores)
    _, p_norm_diff = stats.shapiro(rotating_anchor_scores - llm_only_scores)
    
    print(f"  Normality (Shapiro-Wilk):")
    print(f"    LLM-Only: p = {p_norm_llm:.4f} {'✓' if p_norm_llm > 0.05 else '✗'}")
    print(f"    Rotating Anchor: p = {p_norm_ra:.4f} {'✓' if p_norm_ra > 0.05 else '✗'}")
    print(f"    Difference scores: p = {p_norm_diff:.4f} {'✓' if p_norm_diff > 0.05 else '✗'}")
    
    # If normality violated, also report Wilcoxon
    if p_norm_diff < 0.05:
        print(f"\n  Non-parametric alternative (Wilcoxon signed-rank):")
        w_stat, w_p = stats.wilcoxon(llm_only_scores, rotating_anchor_scores)
        print(f"    W = {w_stat:.3f}, p = {w_p:.4f}")
    
    return {
        'llm_only_mean': llm_only_scores.mean(),
        'rotating_anchor_mean': rotating_anchor_scores.mean(),
        't_stat': t_stat,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'llm_only_scores': llm_only_scores,
        'rotating_anchor_scores': rotating_anchor_scores
    }

def secondary_analysis(data):
    """Preference proportions and explanations"""
    
    print("\n" + "="*60)
    print("SECONDARY ANALYSIS: Condition Preferences")
    print("="*60)
    
    preferences = pd.DataFrame([
        {
            'participant_id': pref['participant_id'],
            'preferred_condition': pref['preferred_condition'],
            'explanation': pref['explanation']
        }
        for pref in data['final_preferences']
    ])
    
    # Count preferences
    pref_counts = preferences['preferred_condition'].value_counts()
    
    print(f"\nPreference Distribution (N={len(preferences)}):")
    for condition, count in pref_counts.items():
        percentage = (count / len(preferences)) * 100
        print(f"  {condition}: {count} ({percentage:.1f}%)")
    
    # Binomial test (against 50-50 chance)
    if 'llm_only' in pref_counts and 'rotating_anchor' in pref_counts:
        llm_count = pref_counts.get('llm_only', 0)
        ra_count = pref_counts.get('rotating_anchor', 0)
        total_chose = llm_count + ra_count  # Exclude "both_equal"
        
        p_binom = stats.binom_test(max(llm_count, ra_count), total_chose, 0.5)
        print(f"\nBinomial test (H0: 50-50 split):")
        print(f"  p = {p_binom:.4f} {'*' if p_binom < 0.05 else '(ns)'}")
    
    # Sample explanations
    print(f"\nSample Preference Explanations:")
    for _, row in preferences.head(3).iterrows():
        print(f"\n  {row['participant_id']} ({row['preferred_condition']}):")
        print(f"    \"{row['explanation'][:150]}...\"")
    
    return preferences

def exploratory_analysis(data, scores_df):
    """Additional exploratory analyses"""
    
    print("\n" + "="*60)
    print("EXPLORATORY ANALYSES")
    print("="*60)
    
    # 1. Topic difficulty comparison
    print("\nTopic Difficulty:")
    topic_scores = scores_df.groupby('topic')['score_percentage'].agg(['mean', 'std'])
    for topic, row in topic_scores.iterrows():
        topic_name = "Lazy/Eager" if "lazy" in topic else "Parallelism"
        print(f"  {topic_name}: M = {row['mean']:.2f}%, SD = {row['std']:.2f}%")
    
    # 2. Order effects
    print("\nOrder Effects (Module 1 vs Module 2):")
    module_scores = scores_df.groupby('module_number')['score_percentage'].agg(['mean', 'std'])
    for module, row in module_scores.iterrows():
        print(f"  Module {module}: M = {row['mean']:.2f}%, SD = {row['std']:.2f}%")
    
    # 3. Individual patterns
    print("\nIndividual Patterns:")
    pivot = scores_df.pivot_table(
        index='participant_id',
        columns='condition',
        values='score_percentage'
    )
    pivot['difference'] = pivot['rotating_anchor'] - pivot['llm_only']
    pivot['favors'] = pivot['difference'].apply(lambda x: 'RA' if x > 0 else 'LLM' if x < 0 else 'Equal')
    
    favors_counts = pivot['favors'].value_counts()
    print(f"  Participants scoring higher in RA: {favors_counts.get('RA', 0)}")
    print(f"  Participants scoring higher in LLM: {favors_counts.get('LLM', 0)}")
    print(f"  Equal scores: {favors_counts.get('Equal', 0)}")

def create_visualizations(results, preferences, scores_df):
    """Create publication-quality figures for CW3"""
    
    print("\n" + "="*60)
    print("Creating visualizations...")
    print("="*60)
    
    # Figure 1: Condition Comparison (Bar chart with error bars)
    fig, ax = plt.subplots(figsize=(8, 6))
    
    conditions = ['LLM-Only', 'Rotating Anchor']
    means = [results['llm_only_mean'], results['rotating_anchor_mean']]
    sds = [results['llm_only_scores'].std(), results['rotating_anchor_scores'].std()]
    
    bars = ax.bar(conditions, means, yerr=sds, capsize=10, 
                   color=['#3498db', '#e74c3c'], alpha=0.7, edgecolor='black')
    
    ax.set_ylabel('Quiz Score (%)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Condition', fontsize=14, fontweight='bold')
    ax.set_title('Learning Outcomes by Condition (N=16)', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.axhline(y=50, color='gray', linestyle='--', alpha=0.5, label='Chance level')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig('figure1_condition_comparison.png', dpi=300, bbox_inches='tight')
    print("  ✓ figure1_condition_comparison.png saved")
    
    # Figure 2: Individual Differences (Paired plot)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    for idx, participant in enumerate(results['llm_only_scores'].index):
        llm_score = results['llm_only_scores'][participant]
        ra_score = results['rotating_anchor_scores'][participant]
        
        ax.plot([1, 2], [llm_score, ra_score], 'o-', 
                color='gray', alpha=0.5, linewidth=1)
    
    # Add means
    ax.plot([1, 2], [results['llm_only_mean'], results['rotating_anchor_mean']],
            'o-', color='red', linewidth=3, markersize=12, label='Mean')
    
    ax.set_xticks([1, 2])
    ax.set_xticklabels(['LLM-Only', 'Rotating Anchor'], fontsize=12)
    ax.set_ylabel('Quiz Score (%)', fontsize=14, fontweight='bold')
    ax.set_title('Individual Participant Trajectories (N=16)', fontsize=16, fontweight='bold')
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('figure2_individual_patterns.png', dpi=300, bbox_inches='tight')
    print("  ✓ figure2_individual_patterns.png saved")
    
    # Figure 3: Preference Distribution (Pie chart)
    fig, ax = plt.subplots(figsize=(8, 8))
    
    pref_counts = preferences['preferred_condition'].value_counts()
    labels = [
        f"LLM-Only\n({pref_counts.get('llm_only', 0)} participants)",
        f"Rotating Anchor\n({pref_counts.get('rotating_anchor', 0)} participants)",
        f"Both Equal\n({pref_counts.get('both_equal', 0)} participants)"
    ]
    sizes = [
        pref_counts.get('llm_only', 0),
        pref_counts.get('rotating_anchor', 0),
        pref_counts.get('both_equal', 0)
    ]
    colors = ['#3498db', '#e74c3c', '#95a5a6']
    
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
           startangle=90, textprops={'fontsize': 12, 'fontweight': 'bold'})
    ax.set_title('Condition Preference Distribution (N=16)', 
                 fontsize=16, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('figure3_preferences.png', dpi=300, bbox_inches='tight')
    print("  ✓ figure3_preferences.png saved")
    
    print("\nAll figures saved! Include these in your CW3 report.")

def generate_cw3_results_text(results, preferences):
    """Generate formatted text for CW3 Results section"""
    
    print("\n" + "="*60)
    print("FORMATTED TEXT FOR CW3 RESULTS SECTION")
    print("="*60)
    
    text = f"""
RESULTS

Primary Analysis: Learning Outcomes

A paired-samples t-test compared learning outcomes (quiz scores) between 
the LLM-Only Facilitator condition (M = {results['llm_only_mean']:.2f}%, 
SD = {results['llm_only_scores'].std():.2f}%) and the Rotating Anchor with 
LLM Coaching condition (M = {results['rotating_anchor_mean']:.2f}%, 
SD = {results['rotating_anchor_scores'].std():.2f}%).

{'There was a statistically significant difference' if results['p_value'] < 0.05 else 'There was no statistically significant difference'} 
between conditions, t({len(results['llm_only_scores'])-1}) = {results['t_stat']:.3f}, 
p = {results['p_value']:.4f}, Cohen's d = {results['cohens_d']:.3f}. 
The effect size was {
    'negligible' if abs(results['cohens_d']) < 0.2 else
    'small' if abs(results['cohens_d']) < 0.5 else
    'medium' if abs(results['cohens_d']) < 0.8 else
    'large'
}.

Figure 1 shows the mean quiz scores for each condition with error bars 
representing one standard deviation. Figure 2 displays individual participant 
trajectories, revealing {'considerable' if results['rotating_anchor_scores'].std() > 15 else 'moderate'} 
variability in condition effects across participants.

Secondary Analysis: Condition Preferences

Participant preferences were distributed as follows: 
{preferences['preferred_condition'].value_counts().get('llm_only', 0)} participants 
preferred the LLM-Only condition, 
{preferences['preferred_condition'].value_counts().get('rotating_anchor', 0)} preferred 
the Rotating Anchor condition, and 
{preferences['preferred_condition'].value_counts().get('both_equal', 0)} rated both 
conditions as equally effective (see Figure 3).

[Continue with thematic analysis of preference explanations...]
    """
    
    print(text)
    
    with open('cw3_results_draft.txt', 'w') as f:
        f.write(text)
    
    print("\n✓ Draft results text saved to cw3_results_draft.txt")

def main():
    """Run complete analysis pipeline"""
    
    print("\n" + "="*60)
    print("CW3 DATA ANALYSIS PIPELINE")
    print("="*60)
    
    # Load data
    print("\nLoading data...")
    data = load_data('study_data.json')
    print(f"  ✓ Loaded data for {len(data['participants'])} participants")
    
    # Calculate scores
    print("\nCalculating quiz scores...")
    scores_df = calculate_quiz_scores(data)
    print(f"  ✓ Calculated scores for {len(scores_df)} sessions")
    
    # Run analyses
    results = primary_analysis(scores_df)
    preferences = secondary_analysis(data)
    exploratory_analysis(data, scores_df)
    
    # Create visualizations
    create_visualizations(results, preferences, scores_df)
    
    # Generate CW3 text
    generate_cw3_results_text(results, preferences)
    
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review all figures (figure1, figure2, figure3)")
    print("2. Copy cw3_results_draft.txt into your report")
    print("3. Add thematic analysis of preference explanations")
    print("4. Write Discussion section interpreting these findings")
    print("\nGood luck with CW3! 🎯")

if __name__ == "__main__":
    main()
