"""
Wikipedia Language Equity Analysis Tool - Corrected Version

Implements proper methodology:
- Analyzes predefined 40 target languages (30 major + 10 low-resource)
- Focuses on 50 time-sensitive topics
- Ensures consistent language coverage across all topics
- Records missing pages (coverage gaps)

Version: 2.1 (Corrected)
"""

import requests
import pandas as pd
from datetime import datetime
import time
from pathlib import Path
import logging
import json
import hashlib
from typing import Dict, List, Optional, Set

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CorrectedWikipediaAnalyzer:
    """
    Wikipedia analyzer with proper language targeting.
    
    Key improvements:
    - Analyzes specific 40 target languages for all topics
    - Records coverage gaps (missing pages)
    - Distinguishes major vs low-resource languages
    """
    
    def __init__(self, target_languages_file="target_languages_40.txt", cache_dir="cache"):
        """Initialize with predefined target languages."""
        self.base_url = "https://{}.wikipedia.org/w/api.php"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WikipediaLanguageEquityBot/2.1 (Educational Research)'
        })
        
        # Initialize language sets BEFORE loading
        self.major_languages = set()
        self.low_resource_languages = set()
        
        # Load target languages
        self.target_languages = self._load_target_languages(target_languages_file)
        
        logger.info(f"Loaded {len(self.target_languages)} target languages")
        logger.info(f"Major languages: {len(self.major_languages)}")
        logger.info(f"Low-resource languages: {len(self.low_resource_languages)}")
        
        # Setup directories
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.stats = {
            'api_calls': 0,
            'cache_hits': 0,
            'cache_misses': 0
        }
    
    def _load_target_languages(self, filepath: str) -> Set[str]:
        """Load target language codes from file."""
        languages = set()
        current_section = None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    
                    # Track sections
                    if 'MAJOR LANGUAGES' in line:
                        current_section = 'major'
                        continue
                    elif 'LOW-RESOURCE LANGUAGES' in line:
                        current_section = 'low_resource'
                        continue
                    
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Extract language code (first word before space or comment)
                    lang_code = line.split()[0].split('#')[0].strip()
                    
                    if lang_code:
                        languages.add(lang_code)
                        
                        # Categorize
                        if current_section == 'major':
                            self.major_languages.add(lang_code)
                        elif current_section == 'low_resource':
                            self.low_resource_languages.add(lang_code)
            
            logger.info(f"Successfully loaded {len(languages)} target languages")
            return languages
            
        except FileNotFoundError:
            logger.error(f"Target languages file not found: {filepath}")
            logger.info("Using default 40 languages")
            # Default fallback
            major = {'en','zh','es','fr','de','ja','ru','pt','it','ar','pl','nl','tr',
                    'sv','uk','fa','ko','vi','cs','he','id','fi','th','no','ro','hu',
                    'da','el','bg','sr'}
            low_res = {'sw','hi','bn','ha','am','my','ne','si','ur','ps'}
            
            self.major_languages = major
            self.low_resource_languages = low_res
            return major | low_res
    
    def _cache_key(self, url: str, params: dict) -> str:
        """Generate cache key from URL and parameters."""
        key_string = f"{url}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cached_response(self, cache_key: str) -> Optional[dict]:
        """Retrieve cached API response."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached_data = json.load(f)
                    
                cache_time = datetime.fromisoformat(cached_data['cached_at'])
                age_hours = (datetime.now() - cache_time).total_seconds() / 3600
                
                if age_hours < 24:
                    self.stats['cache_hits'] += 1
                    return cached_data['response']
            except Exception as e:
                logger.warning(f"Cache read error: {e}")
        
        self.stats['cache_misses'] += 1
        return None
    
    def _save_to_cache(self, cache_key: str, response_data: dict):
        """Save API response to cache."""
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        try:
            cache_data = {
                'cached_at': datetime.now().isoformat(),
                'response': response_data
            }
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Cache write error: {e}")
    
    def _api_request(self, url: str, params: dict, max_retries: int = 3) -> Optional[dict]:
        """Make API request with caching and retry logic."""
        cache_key = self._cache_key(url, params)
        
        cached_response = self._get_cached_response(cache_key)
        if cached_response:
            return cached_response
        
        for attempt in range(max_retries):
            try:
                self.stats['api_calls'] += 1
                response = self.session.get(url, params=params, timeout=15)
                response.raise_for_status()
                
                data = response.json()
                self._save_to_cache(cache_key, data)
                
                return data
                
            except requests.exceptions.RequestException as e:
                wait_time = 2 ** attempt
                logger.warning(f"API request failed (attempt {attempt + 1}/{max_retries}): {e}")
                
                if attempt < max_retries - 1:
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Max retries reached. Request failed.")
                    return None
        
        return None
    
    def get_langlinks(self, title: str, lang: str = 'en') -> Dict[str, str]:
        """
        Get interlanguage links and map to target languages.
        
        Returns:
            dict: {lang_code: page_title} for languages that have the page
        """
        logger.info(f"Fetching language links for '{title}'")
        
        url = self.base_url.format(lang)
        params = {
            'action': 'query',
            'prop': 'langlinks',
            'titles': title,
            'lllimit': 'max',
            'format': 'json',
            'formatversion': 2
        }
        
        data = self._api_request(url, params)
        if not data:
            return {}
        
        pages = data.get('query', {}).get('pages', [])
        if not pages or 'langlinks' not in pages[0]:
            logger.warning(f"No interlanguage links found for '{title}'")
            return {}
        
        # Map available languages
        lang_map = {}
        for link in pages[0]['langlinks']:
            lang_code = link['lang']
            if lang_code in self.target_languages:
                lang_map[lang_code] = link['title']
        
        found_count = len(lang_map)
        target_count = len(self.target_languages) - 1  # Exclude English
        logger.info(f"Found {found_count}/{target_count} target languages")
        
        return lang_map
    
    def get_revision_info(self, title: str, lang: str = 'en') -> Dict[str, Optional[str]]:
        """Fetch first and latest revision timestamps."""
        url = self.base_url.format(lang)
        
        params_first = {
            'action': 'query',
            'prop': 'revisions',
            'titles': title,
            'rvprop': 'timestamp',
            'rvlimit': 1,
            'rvdir': 'newer',
            'format': 'json',
            'formatversion': 2
        }
        
        params_latest = {
            'action': 'query',
            'prop': 'revisions',
            'titles': title,
            'rvprop': 'timestamp',
            'rvlimit': 1,
            'rvdir': 'older',
            'format': 'json',
            'formatversion': 2
        }
        
        data_first = self._api_request(url, params_first)
        time.sleep(0.3)
        data_latest = self._api_request(url, params_latest)
        
        first_timestamp = None
        latest_timestamp = None
        
        if data_first:
            pages_first = data_first.get('query', {}).get('pages', [])
            if pages_first and 'revisions' in pages_first[0]:
                first_timestamp = pages_first[0]['revisions'][0]['timestamp']
        
        if data_latest:
            pages_latest = data_latest.get('query', {}).get('pages', [])
            if pages_latest and 'revisions' in pages_latest[0]:
                latest_timestamp = pages_latest[0]['revisions'][0]['timestamp']
        
        return {
            'first_edit': first_timestamp,
            'latest_edit': latest_timestamp
        }
    
    def analyze_topic(self, english_title: str) -> pd.DataFrame:
        """
        Analyze a topic across all 40 target languages.
        
        Records:
        - Pages that exist with timestamps
        - Pages that don't exist (coverage gaps)
        """
        logger.info(f"=" * 60)
        logger.info(f"Analyzing topic: {english_title}")
        logger.info(f"=" * 60)
        
        results = []
        
        # Get English version metadata
        en_info = self.get_revision_info(english_title, 'en')
        en_first = en_info['first_edit']
        en_latest = en_info['latest_edit']
        
        if not en_first:
            logger.warning(f"Cannot fetch English version, skipping '{english_title}'")
            return pd.DataFrame()
        
        logger.info(f"English created: {en_first}")
        logger.info(f"English updated: {en_latest}")
        
        # Record English baseline
        results.append({
            'topic': english_title,
            'language': 'en',
            'language_type': 'baseline',
            'title': english_title,
            'exists': True,
            'first_edit': en_first,
            'latest_edit': en_latest,
            'time_to_presence_days': 0,
            'update_lag_days': 0
        })
        
        # Get available language versions
        lang_map = self.get_langlinks(english_title)
        
        # Analyze each target language
        logger.info(f"Analyzing {len(self.target_languages)-1} target languages...")
        
        for i, lang_code in enumerate(sorted(self.target_languages - {'en'}), 1):
            # Determine language type
            if lang_code in self.major_languages:
                lang_type = 'major'
            elif lang_code in self.low_resource_languages:
                lang_type = 'low_resource'
            else:
                lang_type = 'other'
            
            logger.info(f"[{i}/{len(self.target_languages)-1}] {lang_code} ({lang_type})")
            
            # Check if page exists
            if lang_code not in lang_map:
                logger.warning(f"  Page does not exist in {lang_code}")
                results.append({
                    'topic': english_title,
                    'language': lang_code,
                    'language_type': lang_type,
                    'title': None,
                    'exists': False,
                    'first_edit': None,
                    'latest_edit': None,
                    'time_to_presence_days': None,
                    'update_lag_days': None
                })
                continue
            
            # Page exists - get timestamps
            lang_title = lang_map[lang_code]
            lang_rev_info = self.get_revision_info(lang_title, lang_code)
            
            if lang_rev_info['first_edit'] and lang_rev_info['latest_edit']:
                # Calculate metrics
                en_first_dt = datetime.fromisoformat(en_first.replace('Z', '+00:00'))
                lang_first_dt = datetime.fromisoformat(
                    lang_rev_info['first_edit'].replace('Z', '+00:00')
                )
                
                en_latest_dt = datetime.fromisoformat(en_latest.replace('Z', '+00:00'))
                lang_latest_dt = datetime.fromisoformat(
                    lang_rev_info['latest_edit'].replace('Z', '+00:00')
                )
                
                time_to_presence = (lang_first_dt - en_first_dt).days
                update_lag = (en_latest_dt - lang_latest_dt).days
                
                logger.info(f"  ✓ Time-to-presence: {time_to_presence} days | "
                           f"Update lag: {update_lag} days")
                
                results.append({
                    'topic': english_title,
                    'language': lang_code,
                    'language_type': lang_type,
                    'title': lang_title,
                    'exists': True,
                    'first_edit': lang_rev_info['first_edit'],
                    'latest_edit': lang_rev_info['latest_edit'],
                    'time_to_presence_days': time_to_presence,
                    'update_lag_days': update_lag
                })
            else:
                logger.warning(f"  Unable to retrieve timestamps for {lang_code}")
                results.append({
                    'topic': english_title,
                    'language': lang_code,
                    'language_type': lang_type,
                    'title': lang_title,
                    'exists': True,
                    'first_edit': None,
                    'latest_edit': None,
                    'time_to_presence_days': None,
                    'update_lag_days': None
                })
            
            time.sleep(0.5)
        
        return pd.DataFrame(results)
    
    def save_results(self, df: pd.DataFrame, filename: str):
        """Save results in multiple formats."""
        base_name = filename.replace('.csv', '')
        
        csv_path = self.data_dir / f"{base_name}.csv"
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
        logger.info(f"Saved CSV: {csv_path}")
        
        excel_path = self.data_dir / f"{base_name}.xlsx"
        df.to_excel(excel_path, index=False, engine='openpyxl')
        logger.info(f"Saved Excel: {excel_path}")
        
        try:
            parquet_path = self.data_dir / f"{base_name}.parquet"
            df.to_parquet(parquet_path, index=False, engine='pyarrow')
            logger.info(f"Saved Parquet: {parquet_path}")
        except ImportError:
            logger.warning("Parquet support not available")
        
        return csv_path
    
    def print_cache_stats(self):
        """Print caching statistics."""
        total_requests = self.stats['cache_hits'] + self.stats['cache_misses']
        cache_hit_rate = (self.stats['cache_hits'] / total_requests * 100) if total_requests > 0 else 0
        
        logger.info("\n" + "=" * 60)
        logger.info("CACHE STATISTICS")
        logger.info("=" * 60)
        logger.info(f"Total requests: {total_requests}")
        logger.info(f"Cache hits: {self.stats['cache_hits']} ({cache_hit_rate:.1f}%)")
        logger.info(f"Cache misses: {self.stats['cache_misses']}")
        logger.info(f"API calls made: {self.stats['api_calls']}")
        logger.info("=" * 60)


def load_topics_from_file(filepath='topics_critical_50.txt'):
    """Load topic list from file."""
    topics = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    topics.append(line)
        logger.info(f"Loaded {len(topics)} topics from {filepath}")
        return topics
    except FileNotFoundError:
        logger.error(f"Topics file not found: {filepath}")
        return []


def generate_summary_report(df: pd.DataFrame):
    """Generate comprehensive summary with major vs low-resource comparison."""
    logger.info("=" * 60)
    logger.info("ANALYSIS SUMMARY")
    logger.info("=" * 60)
    
    logger.info(f"Total topics analyzed: {df['topic'].nunique()}")
    logger.info(f"Total languages: {df['language'].nunique()}")
    logger.info(f"Total records: {len(df)}")
    
    # Coverage analysis
    coverage = df[df['exists'] == True].groupby('language').size()
    total_topics = df['topic'].nunique()
    
    logger.info(f"\nCoverage by language type:")
    for lang_type in ['major', 'low_resource']:
        type_df = df[df['language_type'] == lang_type]
        if not type_df.empty:
            avg_coverage = (type_df['exists'].sum() / len(type_df) * 100)
            logger.info(f"  {lang_type}: {avg_coverage:.1f}% average coverage")
    
    # Update lag comparison
    existing = df[(df['exists'] == True) & (df['language'] != 'en')]
    
    if not existing.empty:
        logger.info(f"\nUpdate lag statistics:")
        logger.info(f"  Overall mean: {existing['update_lag_days'].mean():.1f} days")
        logger.info(f"  Overall median: {existing['update_lag_days'].median():.1f} days")
        
        for lang_type in ['major', 'low_resource']:
            type_data = existing[existing['language_type'] == lang_type]
            if not type_data.empty:
                logger.info(f"  {lang_type} mean: {type_data['update_lag_days'].mean():.1f} days")
    
    # Missing pages
    missing = df[df['exists'] == False]
    if not missing.empty:
        logger.info(f"\nCoverage gaps:")
        logger.info(f"  Total missing pages: {len(missing)}")
        logger.info(f"  Percent missing: {len(missing)/len(df)*100:.1f}%")
        
        # Most missing topics
        missing_by_topic = missing.groupby('topic').size().sort_values(ascending=False)
        logger.info(f"\n  Topics with most gaps (top 5):")
        for topic, count in missing_by_topic.head(5).items():
            logger.info(f"    {topic}: missing in {count} languages")


def main():
    """Main execution function."""
    
    logger.info("Wikipedia Language Equity Analysis Tool v2.1 (Corrected)")
    logger.info("=" * 60)
    logger.info("Methodology: 40 predefined target languages × 50 critical topics")
    logger.info("=" * 60)
    
    # Load topics
    topics = load_topics_from_file('topics_critical_50.txt')
    
    if not topics:
        logger.error("No topics to analyze")
        return
    
    logger.info(f"Will analyze {len(topics)} time-sensitive topics")
    
    # Initialize corrected analyzer
    analyzer = CorrectedWikipediaAnalyzer('target_languages_40.txt')
    all_results = []
    
    # Analyze each topic
    start_time = time.time()
    
    for i, topic in enumerate(topics, 1):
        logger.info(f"\n{'#' * 60}")
        logger.info(f"Progress: {i}/{len(topics)} ({i/len(topics)*100:.1f}%)")
        logger.info(f"{'#' * 60}")
        
        df = analyzer.analyze_topic(topic)
        if not df.empty:
            all_results.append(df)
        
        time.sleep(1)
    
    elapsed_time = time.time() - start_time
    
    # Combine and save results
    if all_results:
        final_df = pd.concat(all_results, ignore_index=True)
        analyzer.save_results(final_df, 'language_equity_analysis_v2')
        
        # Generate summary
        generate_summary_report(final_df)
        
        # Show cache statistics
        analyzer.print_cache_stats()
        
        logger.info(f"\nTotal analysis time: {elapsed_time/60:.1f} minutes")
        logger.info("\n" + "=" * 60)
        logger.info("Analysis complete!")
        logger.info("=" * 60)
        logger.info("\nNext steps:")
        logger.info("  1. Check 'data' directory for results")
        logger.info("  2. Run 'python visualize_results.py data/language_equity_analysis_v2.csv'")
    else:
        logger.error("No data collected")


if __name__ == "__main__":
    main()
