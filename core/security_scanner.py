import os
import re
import json
from typing import List, Dict

class SecurityScanner:
    def __init__(self):
        self.security_issues = []
        
    def scan_repository(self, repo_path: str) -> Dict:
        """Scan repository for security issues"""
        self.security_issues = []
        
        # Scan for secrets
        self._scan_secrets(repo_path)
        
        # Scan for dangerous commands
        self._scan_dangerous_commands(repo_path)
        
        # Scan dependencies
        self._scan_dependencies(repo_path)
        
        return {
            'total_issues': len(self.security_issues),
            'issues': self.security_issues,
            'risk_level': self._calculate_risk_level()
        }
    
    def _scan_secrets(self, repo_path: str):
        """Scan for potential secrets in files"""
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']+["\']', 'Hardcoded password'),
            (r'api_key\s*=\s*["\'][^"\']+["\']', 'API key'),
            (r'secret\s*=\s*["\'][^"\']+["\']', 'Secret token'),
            (r'token\s*=\s*["\'][^"\']+["\']', 'Access token'),
            (r'[A-Za-z0-9]{32,}', 'Potential hash/key')
        ]
        
        for root, dirs, files in os.walk(repo_path):
            # Skip .git directory
            if '.git' in dirs:
                dirs.remove('.git')
                
            for file in files:
                if file.endswith(('.py', '.js', '.yml', '.yaml', '.json', '.env')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        for pattern, description in secret_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            if matches:
                                self.security_issues.append({
                                    'type': 'secret',
                                    'file': file_path.replace(repo_path, ''),
                                    'description': description,
                                    'severity': 'HIGH'
                                })
                    except Exception:
                        continue
    
    def _scan_dangerous_commands(self, repo_path: str):
        """Scan for dangerous commands in pipeline files"""
        dangerous_commands = [
            'rm -rf /',
            'sudo',
            'curl | sh',
            'wget | sh',
            'eval',
            'exec',
            'system(',
            'shell_exec'
        ]
        
        pipeline_files = ['.cicd.yml', '.github/workflows/*.yml', 'Dockerfile']
        
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.yml', '.yaml', 'Dockerfile')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                        for cmd in dangerous_commands:
                            if cmd in content:
                                self.security_issues.append({
                                    'type': 'dangerous_command',
                                    'file': file_path.replace(repo_path, ''),
                                    'description': f'Dangerous command: {cmd}',
                                    'severity': 'CRITICAL'
                                })
                    except Exception:
                        continue
    
    def _scan_dependencies(self, repo_path: str):
        """Scan for known vulnerable dependencies"""
        # Check requirements.txt
        req_file = os.path.join(repo_path, 'requirements.txt')
        if os.path.exists(req_file):
            try:
                with open(req_file, 'r') as f:
                    deps = f.read()
                    
                # Simple check for old versions
                if 'django==1.' in deps or 'flask==0.' in deps:
                    self.security_issues.append({
                        'type': 'vulnerable_dependency',
                        'file': '/requirements.txt',
                        'description': 'Potentially outdated dependencies',
                        'severity': 'MEDIUM'
                    })
            except Exception:
                pass
    
    def _calculate_risk_level(self) -> str:
        """Calculate overall risk level"""
        if not self.security_issues:
            return 'LOW'
        
        critical_count = sum(1 for issue in self.security_issues if issue['severity'] == 'CRITICAL')
        high_count = sum(1 for issue in self.security_issues if issue['severity'] == 'HIGH')
        
        if critical_count > 0:
            return 'CRITICAL'
        elif high_count > 2:
            return 'HIGH'
        elif len(self.security_issues) > 5:
            return 'MEDIUM'
        else:
            return 'LOW'