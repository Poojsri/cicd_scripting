import yaml
import os
import subprocess
from typing import Dict, List, Optional
from urllib.parse import urlparse

from config.settings import PIPELINE_FILE, WORKSPACE_DIR

class PipelineParser:
    def __init__(self):
        self.workspace_dir = WORKSPACE_DIR
        os.makedirs(self.workspace_dir, exist_ok=True)
    
    def clone_repo(self, repo_url: str, commit_sha: str, branch: str) -> str:
        """Clone repository and return local path"""
        repo_name = self._get_repo_name(repo_url)
        local_path = os.path.join(self.workspace_dir, f"{repo_name}_{commit_sha[:8]}")
        
        if os.path.exists(local_path):
            subprocess.run(['rmdir', '/s', '/q', local_path], shell=True, check=False)
        
        # Clone repository
        subprocess.run([
            'git', 'clone', '--depth', '1', '--branch', branch, 
            repo_url, local_path
        ], check=True)
        
        # Checkout specific commit
        subprocess.run(['git', 'checkout', commit_sha], cwd=local_path, check=True)
        
        return local_path
    
    def parse_pipeline(self, repo_path: str) -> Dict:
        """Parse .cicd.yml file from repository"""
        pipeline_file = os.path.join(repo_path, PIPELINE_FILE)
        
        if not os.path.exists(pipeline_file):
            return self._default_pipeline()
        
        with open(pipeline_file, 'r') as f:
            return yaml.safe_load(f)
    
    def _get_repo_name(self, repo_url: str) -> str:
        """Extract repository name from URL"""
        parsed = urlparse(repo_url)
        return parsed.path.strip('/').replace('/', '_').replace('.git', '')
    
    def _default_pipeline(self) -> Dict:
        """Default pipeline if no .cicd.yml found"""
        return {
            'name': 'default',
            'steps': [
                {'name': 'install', 'run': 'pip install -r requirements.txt'},
                {'name': 'test', 'run': 'python -m pytest'}
            ]
        }
    
    def validate_pipeline(self, pipeline: Dict) -> bool:
        """Validate pipeline structure"""
        required_fields = ['name', 'steps']
        if not all(field in pipeline for field in required_fields):
            return False
        
        for step in pipeline['steps']:
            if not isinstance(step, dict) or 'name' not in step or 'run' not in step:
                return False
        
        return True