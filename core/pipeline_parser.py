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
        """Clone or pull repository and return local path"""
        repo_name = self._get_repo_name(repo_url)
        local_path = os.path.abspath(os.path.join(self.workspace_dir, repo_name))
        
        try:
            if os.path.exists(local_path):
                # Repository exists, just pull latest
                subprocess.run(['git', 'fetch', 'origin'], cwd=local_path, check=True, capture_output=True)
                subprocess.run(['git', 'checkout', branch], cwd=local_path, check=True, capture_output=True)
                subprocess.run(['git', 'pull', 'origin', branch], cwd=local_path, check=True, capture_output=True)
            else:
                # Clone repository - try without branch first
                try:
                    subprocess.run(['git', 'clone', repo_url, local_path], check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    # Try with branch specification
                    subprocess.run(['git', 'clone', '--branch', branch, repo_url, local_path], check=True, capture_output=True)
            
            # Checkout specific commit if provided and different from branch
            if commit_sha != branch and len(commit_sha) > 10:  # Looks like a real commit SHA
                try:
                    subprocess.run(['git', 'checkout', commit_sha], cwd=local_path, check=True, capture_output=True)
                except subprocess.CalledProcessError:
                    # Commit might not exist, stay on branch
                    pass
            
            return local_path
            
        except subprocess.CalledProcessError as e:
            raise Exception(f"Git operation failed: {e}")
    
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
                {'name': 'check_python', 'run': 'python --version'},
                {'name': 'list_files', 'run': 'dir' if os.name == 'nt' else 'ls -la'},
                {'name': 'test_echo', 'run': 'echo "Pipeline completed successfully!"'}
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