"""
Wikipedia Language Equity Visualization Dashboard

Generates interactive visualizations including:
- Heatmap of update lags (languages × topics)
- Coverage bar charts
- Language ranking tables
- Time-series plots

Requirements: plotly, pandas
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LanguageEquityDashboard:
    """Generate interactive visualizations from analysis results."""
    
    def __init__(self, data_file):
        """
        Initialize dashboard with analysis data.
        
        Args:
            data_file (str): Path to CSV file with analysis results
        """
        self.df = pd.read_csv(data_file)
        self.output_dir = Path("visualizations")
        self.output_dir.mkdir(exist_ok=True)
        logger.info(f"Loaded {len(self.df)} records from {data_file}")
    
    def create_update_lag_heatmap(self):
        """
        Create heatmap showing update lag for each language-topic pair.
        
        Returns:
            plotly.graph_objects.Figure: Interactive heatmap
        """
        logger.info("Creating update lag heatmap...")
        
        # Filter out English (baseline)
        df_pivot = self.df[self.df['language'] != 'en'].copy()
        
        # Create pivot table
        pivot = df_pivot.pivot_table(
            values='update_lag_days',
            index='language',
            columns='topic',
            aggfunc='mean'
        )
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale='RdYlGn_r',  # Red = bad (high lag), Green = good (low lag)
            colorbar=dict(title="Days Behind English"),
            text=pivot.values.round(0),
            texttemplate='%{text}',
            textfont={"size": 8},
            hovertemplate='<b>%{y}</b><br>%{x}<br>Lag: %{z:.0f} days<extra></extra>'
        ))
        
        fig.update_layout(
            title='Wikipedia Update Lag: Days Behind English Version',
            xaxis_title='Topic',
            yaxis_title='Language',
            height=max(400, len(pivot.index) * 30),
            width=max(1200, len(pivot.columns) * 50),
            xaxis={'tickangle': 45},
            font=dict(size=10)
        )
        
        output_path = self.output_dir / "update_lag_heatmap.html"
        fig.write_html(output_path)
        logger.info(f"Saved heatmap to {output_path}")
        
        return fig
    
    def create_coverage_chart(self):
        """
        Create bar chart showing coverage rate by language.
        
        Returns:
            plotly.graph_objects.Figure: Coverage bar chart
        """
        logger.info("Creating coverage bar chart...")
        
        # Calculate coverage per language
        total_topics = self.df[self.df['language'] == 'en']['topic'].nunique()
        coverage = self.df.groupby('language')['topic'].nunique().reset_index()
        coverage.columns = ['language', 'topics_covered']
        coverage['coverage_rate'] = (coverage['topics_covered'] / total_topics * 100).round(1)
        coverage = coverage.sort_values('coverage_rate', ascending=True)
        
        # Create bar chart
        fig = px.bar(
            coverage,
            x='coverage_rate',
            y='language',
            orientation='h',
            text='topics_covered',
            title='Language Coverage: Number of Topics Available',
            labels={'coverage_rate': 'Coverage Rate (%)', 'language': 'Language'},
            color='coverage_rate',
            color_continuous_scale='Blues'
        )
        
        fig.update_traces(
            texttemplate='%{text} topics',
            textposition='outside'
        )
        
        fig.update_layout(
            height=max(400, len(coverage) * 25),
            showlegend=False,
            xaxis_range=[0, 105]
        )
        
        output_path = self.output_dir / "coverage_chart.html"
        fig.write_html(output_path)
        logger.info(f"Saved coverage chart to {output_path}")
        
        return fig
    
    def create_lag_distribution(self):
        """
        Create box plot showing distribution of update lags by language.
        
        Returns:
            plotly.graph_objects.Figure: Box plot
        """
        logger.info("Creating lag distribution plot...")
        
        df_non_en = self.df[self.df['language'] != 'en'].copy()
        
        # Sort by median lag
        median_lags = df_non_en.groupby('language')['update_lag_days'].median().sort_values()
        sorted_langs = median_lags.index.tolist()
        
        fig = px.box(
            df_non_en,
            x='language',
            y='update_lag_days',
            title='Distribution of Update Lags by Language',
            labels={'update_lag_days': 'Days Behind English', 'language': 'Language'},
            category_orders={'language': sorted_langs}
        )
        
        fig.update_layout(
            height=600,
            xaxis={'tickangle': 45}
        )
        
        output_path = self.output_dir / "lag_distribution.html"
        fig.write_html(output_path)
        logger.info(f"Saved lag distribution to {output_path}")
        
        return fig
    
    def create_top_lagged_topics(self, top_n=10):
        """
        Create bar chart of most lagged topic-language pairs.
        
        Args:
            top_n (int): Number of top cases to show
            
        Returns:
            plotly.graph_objects.Figure: Bar chart
        """
        logger.info(f"Creating top {top_n} lagged topics chart...")
        
        df_non_en = self.df[self.df['language'] != 'en'].copy()
        top_lagged = df_non_en.nlargest(top_n, 'update_lag_days')
        
        top_lagged['label'] = (
            top_lagged['language'] + ' - ' + 
            top_lagged['topic'].str[:30] + '...'
        )
        
        fig = px.bar(
            top_lagged,
            x='update_lag_days',
            y='label',
            orientation='h',
            title=f'Top {top_n} Most Outdated Pages',
            labels={'update_lag_days': 'Days Behind English', 'label': ''},
            color='update_lag_days',
            color_continuous_scale='Reds'
        )
        
        fig.update_layout(
            height=max(400, top_n * 40),
            showlegend=False,
            yaxis={'autorange': 'reversed'}
        )
        
        output_path = self.output_dir / "top_lagged_topics.html"
        fig.write_html(output_path)
        logger.info(f"Saved top lagged topics to {output_path}")
        
        return fig
    
    def create_time_to_translation(self):
        """
        Create scatter plot of time-to-translation vs update lag.
        
        Returns:
            plotly.graph_objects.Figure: Scatter plot
        """
        logger.info("Creating time-to-translation scatter plot...")
        
        df_non_en = self.df[self.df['language'] != 'en'].copy()
        
        fig = px.scatter(
            df_non_en,
            x='time_to_presence_days',
            y='update_lag_days',
            color='language',
            hover_data=['topic', 'title'],
            title='Translation Delay vs Update Lag',
            labels={
                'time_to_presence_days': 'Days to Create Translation',
                'update_lag_days': 'Days Behind in Updates'
            }
        )
        
        fig.update_layout(height=600, width=1000)
        
        output_path = self.output_dir / "translation_delay_scatter.html"
        fig.write_html(output_path)
        logger.info(f"Saved scatter plot to {output_path}")
        
        return fig
    
    def create_summary_dashboard(self):
        """
        Create comprehensive dashboard with multiple subplots.
        
        Returns:
            plotly.graph_objects.Figure: Combined dashboard
        """
        logger.info("Creating summary dashboard...")
        
        # Calculate summary statistics
        total_topics = self.df[self.df['language'] == 'en']['topic'].nunique()
        total_languages = self.df['language'].nunique() - 1  # Exclude English
        
        df_non_en = self.df[self.df['language'] != 'en']
        avg_lag = df_non_en['update_lag_days'].mean()
        median_lag = df_non_en['update_lag_days'].median()
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=(
                'Average Update Lag by Language',
                'Coverage Rate by Language',
                'Update Lag Distribution',
                'Time to Translation'
            ),
            specs=[
                [{'type': 'bar'}, {'type': 'bar'}],
                [{'type': 'box'}, {'type': 'scatter'}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 1. Average lag by language
        avg_by_lang = df_non_en.groupby('language')['update_lag_days'].mean().sort_values()
        fig.add_trace(
            go.Bar(x=avg_by_lang.values, y=avg_by_lang.index, orientation='h',
                   marker_color='lightcoral', name='Avg Lag'),
            row=1, col=1
        )
        
        # 2. Coverage rate
        coverage = self.df.groupby('language')['topic'].nunique()
        coverage_pct = (coverage / total_topics * 100).sort_values()
        fig.add_trace(
            go.Bar(x=coverage_pct.values, y=coverage_pct.index, orientation='h',
                   marker_color='lightblue', name='Coverage'),
            row=1, col=2
        )
        
        # 3. Update lag distribution
        for lang in df_non_en['language'].unique()[:10]:  # Top 10 languages
            lang_data = df_non_en[df_non_en['language'] == lang]
            fig.add_trace(
                go.Box(y=lang_data['update_lag_days'], name=lang),
                row=2, col=1
            )
        
        # 4. Time to translation scatter
        fig.add_trace(
            go.Scatter(
                x=df_non_en['time_to_presence_days'],
                y=df_non_en['update_lag_days'],
                mode='markers',
                marker=dict(size=5, opacity=0.6),
                text=df_non_en['language'],
                name='Languages'
            ),
            row=2, col=2
        )
        
        # Update layout
        fig.update_layout(
            title_text=f"Wikipedia Language Equity Dashboard<br>" +
                      f"<sub>Total: {total_topics} topics, {total_languages} languages | " +
                      f"Avg lag: {avg_lag:.0f} days | Median lag: {median_lag:.0f} days</sub>",
            height=1000,
            showlegend=False
        )
        
        fig.update_xaxes(title_text="Days", row=1, col=1)
        fig.update_xaxes(title_text="Coverage %", row=1, col=2)
        fig.update_xaxes(title_text="Days to Translation", row=2, col=2)
        fig.update_yaxes(title_text="Days Behind", row=2, col=1)
        fig.update_yaxes(title_text="Days Behind", row=2, col=2)
        
        output_path = self.output_dir / "summary_dashboard.html"
        fig.write_html(output_path)
        logger.info(f"Saved summary dashboard to {output_path}")
        
        return fig
    
    def generate_all_visualizations(self):
        """Generate all visualization types."""
        logger.info("=" * 60)
        logger.info("GENERATING ALL VISUALIZATIONS")
        logger.info("=" * 60)
        
        self.create_update_lag_heatmap()
        self.create_coverage_chart()
        self.create_lag_distribution()
        self.create_top_lagged_topics()
        self.create_time_to_translation()
        self.create_summary_dashboard()
        
        logger.info("\n" + "=" * 60)
        logger.info("ALL VISUALIZATIONS GENERATED")
        logger.info(f"Output directory: {self.output_dir.absolute()}")
        logger.info("=" * 60)
        
        # List all generated files
        files = list(self.output_dir.glob("*.html"))
        logger.info(f"\nGenerated {len(files)} visualization files:")
        for f in files:
            logger.info(f"  - {f.name}")


def main():
    """Main function to generate visualizations."""
    import sys
    
    data_file = "data/language_equity_analysis.csv"
    
    if len(sys.argv) > 1:
        data_file = sys.argv[1]
    
    if not Path(data_file).exists():
        logger.error(f"Data file not found: {data_file}")
        logger.info("Please run wikipedia_analyzer_pro.py first to generate data.")
        return
    
    dashboard = LanguageEquityDashboard(data_file)
    dashboard.generate_all_visualizations()
    
    logger.info("\nTo view visualizations, open the HTML files in your browser:")
    logger.info(f"  Start with: visualizations/summary_dashboard.html")


if __name__ == "__main__":
    main()
