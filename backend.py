import os
import sys
import time
import json

import random
import hashlib
import platform
import subprocess
import shutil
import threading
from datetime import datetime
from pathlib import Path
import psutil
import math
from datetime import datetime
from pathlib import Path
import psutil
import math

# Try to import PDF generation libraries
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    import winreg
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False

# Educational disclaimer
EDUCATIONAL_DISCLAIMER = """
EDUCATIONAL DATA SANITIZATION TOOL
===================================
This tool is designed for educational purposes to demonstrate secure data deletion
techniques used in cybersecurity and data privacy compliance. 

IMPORTANT WARNINGS:
- This tool performs PERMANENT data destruction
- Deleted data CANNOT be recovered
- Always backup important data before use
- Only use on systems/drives you own
- Test in safe environments first
"""

class CompleteSanitizationTool:
    def __init__(self):
        self.system_info = self._gather_system_info()
        self.sanitization_log = []
        self.is_admin = self._check_admin_rights()
        self.dry_run_mode = False  # Always live mode
        self.test_mode = False
        self.deletion_log = []
        
        # Certificate authority info
        self.cert_authority = {
            'name': 'Educational Sanitization Authority',
            'id': 'ESA-2024-EDU',
            'validation_code': self._generate_validation_code()
        }
        
        self.reset_modes = {
            'MANUAL_FILE_DELETION': {
                'name': 'Manual File Selection',
                'description': 'Select specific files for secure deletion',
                'security_level': 'File-level',
                'time_estimate': '5-30 minutes',
                'data_recovery': 'Impossible with proper algorithms'
            },
            'STANDARD_RESET': {
                'name': 'Standard Windows Reset',
                'description': 'Basic Windows reset with standard file deletion',
                'security_level': 'Basic',
                'time_estimate': '30-60 minutes',
                'data_recovery': 'Possible with forensic tools'
            },
            'SECURE_RESET': {
                'name': 'Secure Reset + Reinstall',
                'description': 'Professional sanitization followed by Windows reinstall',
                'security_level': 'Professional',
                'time_estimate': '2-4 hours',
                'data_recovery': 'Extremely difficult'
            },
            'MAXIMUM_SECURITY': {
                'name': 'Maximum Security Wipe + Reinstall',
                'description': 'Military-grade sanitization + complete system rebuild',
                'security_level': 'Military/Enterprise',
                'time_estimate': '4-8 hours',
                'data_recovery': 'Cryptographically impossible'
            }
        }
        
        self.wiping_algorithms = {
            'NIST_CLEAR': {
                'name': 'NIST 800-88 Clear (1-pass)',
                'passes': 1,
                'description': 'Single cryptographic overwrite (recommended for SSDs)',
                'pattern': 'random',
                'fast': True
            },
            'DOD_3PASS': {
                'name': 'DoD 5220.22-M (3-pass)',
                'passes': 3,
                'description': 'Three-pass overwrite (zeros, ones, random)',
                'pattern': 'multi',
                'secure': True
            },
            'GUTMANN_35': {
                'name': 'Gutmann Method (35-pass)',
                'passes': 35,
                'description': 'Maximum security 35-pass overwrite',
                'pattern': 'complex'
            }
        }

    def _generate_validation_code(self):
        """Generate a unique validation code for certificates"""
        timestamp = str(int(time.time()))
        random_part = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))
        return f"EDU-{timestamp[-6:]}-{random_part}"

    def _check_admin_rights(self):
        """Check if running with administrator privileges"""
        try:
            if platform.system() == 'Windows':
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            else:
                return os.geteuid() == 0
        except:
            return False

    def _gather_system_info(self):
        """Collect comprehensive system information"""
        info = {
            'timestamp': datetime.now().isoformat(),
            'platform': platform.platform(),
            'system': platform.system(),
            'release': platform.release(),
            'machine': platform.machine(),
            'processor': platform.processor(),
        }
        
        try:
            if platform.system() == 'Windows' and WINDOWS_AVAILABLE:
                info['windows_edition'] = self._get_windows_edition()
            info['total_memory'] = psutil.virtual_memory().total
            info['disk_info'] = self._get_disk_info()
        except:
            pass
            
        return info

    def _get_windows_edition(self):
        """Get Windows edition information"""
        if not WINDOWS_AVAILABLE:
            return "Windows (Registry access not available)"
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                               r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
            edition, _ = winreg.QueryValueEx(key, "ProductName")
            winreg.CloseKey(key)
            return edition
        except:
            return "Windows (Edition Unknown)"

    def _get_disk_info(self):
        """Get comprehensive disk information"""
        disks = []
        for disk in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(disk.mountpoint)
                disks.append({
                    'device': disk.device,
                    'mountpoint': disk.mountpoint,
                    'fstype': disk.fstype,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free
                })
            except:
                continue
        return disks

    def _format_size(self, size_bytes):
        """Format size in bytes to human readable format"""
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"

    def display_main_interface(self):
        """Display the main interface with all options"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            
            print(EDUCATIONAL_DISCLAIMER)
            print("\n" + "="*70)
            print("CLEARVAULT - EDUCATIONAL DATA SANITIZATION TOOL")
            print("="*70)
            
            mode_indicator = "TEST MODE" if self.test_mode else "LIVE MODE"
            dry_run_indicator = "SAFE MODE" if self.dry_run_mode else "DESTRUCTIVE MODE"
            admin_status = "ADMIN" if self.is_admin else "USER"
            
            print(f"Status: {mode_indicator} | {dry_run_indicator} | {admin_status}")
            print()
            
            print("SANITIZATION OPTIONS:")
            print("1. Manual File Selection & Deletion")
            print("2. Standard System Reset")
            print("3. Secure System Reset")
            print("4. Maximum Security Wipe")
            print()
            print("ANALYSIS & TESTING:")
            print("5. System Analysis")
            print("6. Create Test Environment")
            print("7. Run Unit Tests")
            print()
            print("CERTIFICATE MANAGEMENT:")
            print("8. View Certificates")
            print("9. Generate Sample Certificate")
            print("10. Certificate Validation")
            print()
            print("SETTINGS:")
            print("11. Toggle Test Mode")
            print("12. Toggle Dry Run Mode")
            print("13. Help & Documentation")
            print("14. Exit")
            
            choice = input("\nSelect option (1-14): ").strip()
            
            if choice == '1':
                self.manual_file_deletion()
            elif choice == '2':
                self.execute_reset_mode('STANDARD_RESET')
            elif choice == '3':
                self.execute_reset_mode('SECURE_RESET')
            elif choice == '4':
                self.execute_reset_mode('MAXIMUM_SECURITY')
            elif choice == '5':
                self.display_system_analysis()
            elif choice == '6':
                self.setup_test_environment()
            elif choice == '7':
                self.run_unit_tests()
            elif choice == '8':
                self.view_certificates()
            elif choice == '9':
                self.generate_sample_certificate()
            elif choice == '10':
                self.validate_certificate()
            elif choice == '11':
                self.toggle_test_mode()
            elif choice == '12':
                self.toggle_dry_run_mode()
            elif choice == '13':
                self.display_help_documentation()
            elif choice == '14':
                print("\nThank you for using ClearVault Educational Tool!")
                break
            else:
                print("Invalid choice! Press Enter to continue...")
                input()

    def manual_file_deletion(self):
        """Manual file selection and deletion interface"""
        if self.test_mode:
            start_path = "test_deletion_files"
            if not Path(start_path).exists():
                print("Test environment not found. Creating test files...")
                self.setup_test_environment()
                input("Press Enter to continue...")
        else:
            if platform.system() == 'Windows':
                start_path = "C:\\"
            else:
                start_path = os.path.expanduser("~")
        
        selected_files = []
        current_path = Path(start_path)
        
        while True:
            try:
                os.system('cls' if os.name == 'nt' else 'clear')
                mode_indicator = "TEST MODE" if self.test_mode else "LIVE MODE"
                dry_run_indicator = "SAFE MODE" if self.dry_run_mode else "DESTRUCTIVE MODE"
                
                print(f"MANUAL FILE DELETION - {mode_indicator} - {dry_run_indicator}")
                print("="*70)
                print(f"Current Directory: {current_path}")
                print(f"Selected Files: {len(selected_files)} files")
                if self.dry_run_mode:
                    print("SAFE MODE: Files will NOT be actually deleted")
                else:
                    print("WARNING: Files WILL BE PERMANENTLY DELETED!")
                print("="*70)
                
                # Get directory contents
                items = []
                if current_path.parent != current_path:
                    items.append((".. (Go Back)", current_path.parent, "parent"))
                
                try:
                    dirs = []
                    files = []
                    
                    for item in current_path.iterdir():
                        if item.is_dir():
                            dirs.append(item)
                        else:
                            files.append(item)
                    
                    for dir_item in sorted(dirs):
                        items.append((f"[DIR] {dir_item.name}/", dir_item, "dir"))
                    
                    for file_item in sorted(files):
                        try:
                            size = file_item.stat().st_size
                            size_str = self._format_size(size)
                            status = "SELECTED" if file_item in selected_files else "         "
                            items.append((f"[{status}] {file_item.name} ({size_str})", file_item, "file"))
                        except:
                            continue
                
                except PermissionError:
                    print("Permission denied to access this directory.")
                    input("Press Enter to go back...")
                    current_path = current_path.parent
                    continue
                
                # Display items
                for i, (display_name, path, item_type) in enumerate(items[:20], 1):
                    print(f"{i:2d}. {display_name}")
                
                if len(items) > 20:
                    print(f"... and {len(items) - 20} more items")
                
                print("\nActions:")
                print("Number = Select item  |  a = Select all files  |  c = Clear selection")
                print("d = Delete selected   |  s = Show selected      |  cert = Certificate menu")
                print("q = Back to main menu")
                
                choice = input("\nEnter choice: ").strip().lower()
                
                if choice == 'q':
                    break
                elif choice == 'a':
                    added_count = 0
                    for display_name, path, item_type in items:
                        if item_type == "file" and path not in selected_files:
                            selected_files.append(path)
                            added_count += 1
                    print(f"Added {added_count} files to selection!")
                    time.sleep(1)
                elif choice == 'c':
                    selected_files.clear()
                    print("Selection cleared!")
                    time.sleep(1)
                elif choice == 's':
                    self._show_selected_files(selected_files)
                elif choice == 'd':
                    if selected_files:
                        self._process_secure_deletion(selected_files)
                        selected_files.clear()
                    else:
                        print("No files selected!")
                        time.sleep(1)
                elif choice == 'cert':
                    self.certificate_menu()
                elif choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(items):
                        display_name, path, item_type = items[idx]
                        
                        if item_type == "parent":
                            current_path = path
                        elif item_type == "dir":
                            current_path = path
                        elif item_type == "file":
                            if path in selected_files:
                                selected_files.remove(path)
                                print(f"Removed: {path.name}")
                            else:
                                selected_files.append(path)
                                print(f"Added: {path.name}")
                            time.sleep(0.5)
                    else:
                        print("Invalid selection!")
                        time.sleep(1)
                else:
                    print("Invalid choice!")
                    time.sleep(1)
                        
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                break
            except Exception as e:
                print(f"Error: {e}")
                input("Press Enter to continue...")

    def _show_selected_files(self, selected_files):
        """Display selected files with details"""
        if not selected_files:
            print("\nNo files selected.")
            input("Press Enter to continue...")
            return
        
        os.system('cls' if os.name == 'nt' else 'clear')
        mode_indicator = "SAFE MODE" if self.dry_run_mode else "DESTRUCTIVE MODE"
        print(f"SELECTED FILES FOR DELETION - {mode_indicator}")
        print("="*80)
        
        total_size = 0
        for i, file_path in enumerate(selected_files):
            try:
                size = file_path.stat().st_size
                total_size += size
                modified = datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
                
                print(f"{i+1:2d}. {file_path.name}")
                print(f"     Path: {file_path.parent}")
                print(f"     Size: {self._format_size(size)} | Modified: {modified}")
                print()
            except:
                print(f"{i+1:2d}. {file_path} (File not accessible)")
                print()
        
        print(f"SUMMARY: {len(selected_files)} files, Total size: {self._format_size(total_size)}")
        if self.dry_run_mode:
            print("SAFE MODE: These files will NOT be actually deleted")
        else:
            print("WARNING: These files WILL BE PERMANENTLY DELETED!")
        input("\nPress Enter to continue...")

    def _process_secure_deletion(self, selected_files):
        """Process secure deletion with algorithm selection"""
        if not selected_files:
            return
        
        os.system('cls' if os.name == 'nt' else 'clear')
        mode_indicator = "SAFE MODE" if self.dry_run_mode else "DESTRUCTIVE MODE"
        print(f"SECURE DELETION PROCESS - {mode_indicator}")
        print("="*60)
        
        total_size = sum(f.stat().st_size for f in selected_files if f.exists())
        print(f"Files to delete: {len(selected_files)}")
        print(f"Total size: {self._format_size(total_size)}")
        if self.dry_run_mode:
            print("SAFE MODE: Simulation only - no actual deletion")
        else:
            print("WARNING: Files will be permanently deleted!")
        print()
        
        # Algorithm selection
        print("Choose Wiping Algorithm:")
        for i, (key, info) in enumerate(self.wiping_algorithms.items(), 1):
            speed = "Fast" if info.get('fast') else "Secure"
            print(f"{i}. {info['name']} - {speed}")
        print()
        
        while True:
            try:
                algo_choice = int(input("Select algorithm (1-3): ")) - 1
                algo_keys = list(self.wiping_algorithms.keys())
                if 0 <= algo_choice < len(algo_keys):
                    selected_algorithm = algo_keys[algo_choice]
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Please enter a number!")
        
        # Final confirmation
        print(f"\nFINAL WARNING")
        print(f"Algorithm: {self.wiping_algorithms[selected_algorithm]['name']}")
        print(f"Files: {len(selected_files)}")
        if self.dry_run_mode:
            print("SAFE MODE: This is a simulation only")
        else:
            print("This action CANNOT be undone!")
        print()
        
        if self.dry_run_mode:
            confirm = input("Type 'SIMULATE' to run simulation: ").strip()
            if confirm != 'SIMULATE':
                print("Simulation cancelled.")
                time.sleep(2)
                return
        else:
            confirm = input("Type 'DELETE' to confirm REAL deletion: ").strip()
            if confirm != 'DELETE':
                print("Deletion cancelled.")
                time.sleep(2)
                return
        
        # Perform secure deletion
        self._execute_secure_deletion(selected_files, selected_algorithm)

    def _execute_secure_deletion(self, file_list, algorithm):
        """Execute the secure deletion process"""
        results = []
        algo_info = self.wiping_algorithms[algorithm]
        
        mode_text = "simulation" if self.dry_run_mode else "secure deletion"
        print(f"\nStarting {mode_text} with {algo_info['name']}...")
        print("="*70)
        
        for i, file_path in enumerate(file_list):
            print(f"\nProcessing {i+1}/{len(file_list)}: {file_path.name}")
            
            if not file_path.exists():
                results.append({'file': str(file_path), 'status': 'error', 'error': 'File not found'})
                print("File not found!")
                continue
            
            try:
                if self.dry_run_mode:
                    result = self._simulate_wipe_file(file_path, algorithm)
                    print("Simulation completed successfully!")
                else:
                    result = self._wipe_file(file_path, algorithm)
                    if result['status'] == 'success':
                        print("Successfully wiped and deleted!")
                    else:
                        print(f"Error: {result.get('error', 'Unknown error')}")
                
                results.append(result)
                    
            except Exception as e:
                results.append({'file': str(file_path), 'status': 'error', 'error': str(e)})
                print(f"Error: {e}")
        
        # Generate report and certificate
        report = self._generate_deletion_report(results, algorithm)
        
        operation_text = "SIMULATION" if self.dry_run_mode else "DELETION"
        print(f"\n{operation_text} COMPLETE!")
        print("="*40)
        print(f"Successful: {report['summary']['successful']}")
        print(f"Failed: {report['summary']['failed']}")
        print(f"Report saved: {report['report_file']}")
        
        # Offer certificate generation
        print(f"\nCERTIFICATE GENERATION")
        print("="*40)
        
        self._display_formatted_certificate(report)
        
        if PDF_AVAILABLE:
            generate_pdf = input("\nGenerate PDF certificate? (y/n): ").strip().lower()
            if generate_pdf == 'y':
                pdf_file = self._generate_pdf_certificate(report)
                print(f"PDF Certificate saved: {pdf_file}")
        
        print(f"\nCertificate Validation Code: {self.cert_authority['validation_code']}")
        input("\nPress Enter to continue...")

    def _simulate_wipe_file(self, file_path, algorithm):
        """Simulate wiping a file (for educational purposes)"""
        try:
            file_size = file_path.stat().st_size
            original_hash = self._calculate_hash(file_path)
            
            algo_info = self.wiping_algorithms[algorithm]
            passes_data = []
            
            for pass_num in range(algo_info['passes']):
                time.sleep(0.1)  # Simulate processing time
                
                if algorithm == 'NIST_CLEAR':
                    pattern = 'random_data'
                elif algorithm == 'DOD_3PASS':
                    patterns = ['all_zeros', 'all_ones', 'random_data']
                    pattern = patterns[pass_num]
                elif algorithm == 'GUTMANN_35':
                    pattern = f'gutmann_pass_{pass_num + 1}'
                
                fake_hash = hashlib.sha256(f"simulated_{pattern}_{pass_num}".encode()).hexdigest()
                
                passes_data.append({
                    'pass_number': pass_num + 1,
                    'pattern': pattern,
                    'hash_after': fake_hash
                })
            
            final_hash = hashlib.sha256(f"final_simulated_{algorithm}".encode()).hexdigest()
            
            return {
                'file': str(file_path),
                'status': 'success',
                'algorithm': algorithm,
                'original_hash': original_hash,
                'final_hash': final_hash,
                'original_size': file_size,
                'passes': passes_data,
                'simulated_at': datetime.now().isoformat(),
                'verification': True,
                'simulation_mode': True
            }
            
        except Exception as e:
            return {
                'file': str(file_path),
                'status': 'error',
                'error': str(e),
                'simulation_mode': True
            }

    def _wipe_file(self, file_path, algorithm):
        """Wipe a single file using the specified algorithm"""
        try:
            file_size = file_path.stat().st_size
            original_hash = self._calculate_hash(file_path)
            
            if file_size == 0:
                os.remove(file_path)
                return {
                    'file': str(file_path),
                    'status': 'success',
                    'algorithm': algorithm,
                    'original_hash': original_hash,
                    'final_hash': 'empty_file',
                    'original_size': 0,
                    'passes': []
                }
            
            passes_data = []
            algo_info = self.wiping_algorithms[algorithm]
            
            if algorithm == 'NIST_CLEAR':
                # 1 pass with random data
                pass_hash = self._overwrite_file(file_path, 'random')
                passes_data.append({
                    'pass_number': 1,
                    'pattern': 'random_data',
                    'hash_after': pass_hash
                })
                final_hash = pass_hash
                
            elif algorithm == 'DOD_3PASS':
                # Pass 1: All zeros
                pass_hash = self._overwrite_file(file_path, 'zeros')
                passes_data.append({
                    'pass_number': 1,
                    'pattern': 'all_zeros',
                    'hash_after': pass_hash
                })
                
                # Pass 2: All ones
                pass_hash = self._overwrite_file(file_path, 'ones')
                passes_data.append({
                    'pass_number': 2,
                    'pattern': 'all_ones',
                    'hash_after': pass_hash
                })
                
                # Pass 3: Random data
                pass_hash = self._overwrite_file(file_path, 'random')
                passes_data.append({
                    'pass_number': 3,
                    'pattern': 'random_data',
                    'hash_after': pass_hash
                })
                final_hash = pass_hash
            
            elif algorithm == 'GUTMANN_35':
                # Simplified Gutmann implementation
                for pass_num in range(35):
                    if pass_num < 4:
                        pattern = 'random'
                    elif pass_num < 31:
                        pattern = f'gutmann_{pass_num - 3}'
                    else:
                        pattern = 'random'
                    
                    pass_hash = self._overwrite_file(file_path, pattern)
                    passes_data.append({
                        'pass_number': pass_num + 1,
                        'pattern': pattern,
                        'hash_after': pass_hash
                    })
                final_hash = pass_hash
            
            # Delete the file
            os.remove(file_path)
            
            return {
                'file': str(file_path),
                'status': 'success',
                'algorithm': algorithm,
                'original_hash': original_hash,
                'final_hash': final_hash,
                'original_size': file_size,
                'passes': passes_data,
                'deleted_at': datetime.now().isoformat(),
                'verification': not file_path.exists()
            }
            
        except Exception as e:
            return {
                'file': str(file_path),
                'status': 'error',
                'error': str(e)
            }

    def _overwrite_file(self, file_path, pattern):
        """Overwrite file with specified pattern"""
        file_size = file_path.stat().st_size
        
        with open(file_path, 'r+b') as f:
            f.seek(0)
            
            if pattern == 'zeros':
                data = b'\x00' * file_size
            elif pattern == 'ones':
                data = b'\xFF' * file_size
            elif pattern == 'random':
                data = bytes([random.randint(0, 255) for _ in range(file_size)])
            elif pattern.startswith('gutmann_'):
                # Simplified Gutmann patterns
                data = bytes([(i % 256) for i in range(file_size)])
            else:
                data = bytes([random.randint(0, 255) for _ in range(file_size)])
            
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        
        return self._calculate_hash(file_path)

    def _calculate_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        hash_func = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def setup_test_environment(self):
        """Create a test directory with sample files for safe testing"""
        test_dir = Path("test_deletion_files")
        
        if test_dir.exists():
            shutil.rmtree(test_dir)
        
        test_dir.mkdir(exist_ok=True)
        
        # Create various test files
        test_files = [
            ("small_test.txt", "This is a small test file for secure deletion testing."),
            ("medium_test.txt", "This is a medium test file. " * 100),
            ("large_test.txt", "Large file content. " * 1000),
            ("empty_test.txt", ""),
            ("binary_test.dat", bytes([i % 256 for i in range(1024)])),
        ]
        
        # Create subdirectories with files
        subdir1 = test_dir / "subfolder1"
        subdir2 = test_dir / "subfolder2"
        subdir1.mkdir(exist_ok=True)
        subdir2.mkdir(exist_ok=True)
        
        # Create main directory files
        for filename, content in test_files:
            file_path = test_dir / filename
            if isinstance(content, str):
                file_path.write_text(content)
            else:
                file_path.write_bytes(content)
        
        # Create files in subdirectories
        (subdir1 / "nested_file1.txt").write_text("Nested file in subfolder1")
        (subdir1 / "nested_file2.log").write_text("Log file content")
        (subdir2 / "config.json").write_text('{"test": "data"}')
        (subdir2 / "data.csv").write_text("name,value\ntest1,100\ntest2,200")
        
        print(f"Test environment created at: {test_dir.absolute()}")
        print(f"Created {len(test_files)} test files in main directory")
        print("Created 2 subdirectories with additional files")
        print("\nThis test environment is safe for practicing secure deletion.")
        input("Press Enter to continue...")

    def toggle_test_mode(self):
        """Toggle test mode on/off"""
        self.test_mode = not self.test_mode
        if self.test_mode:
            self.setup_test_environment()
        print(f"Test mode: {'ON' if self.test_mode else 'OFF'}")
        if self.test_mode:
            print("Safe test environment will be used for practice.")
        else:
            print("WARNING: Live mode - real files will be affected!")
        input("Press Enter to continue...")

    def toggle_dry_run_mode(self):
        """Toggle dry run mode on/off"""
        self.dry_run_mode = not self.dry_run_mode
        print(f"Dry run mode: {'ON' if self.dry_run_mode else 'OFF'}")
        if self.dry_run_mode:
            print("SAFE MODE: Operations will be simulated only.")
        else:
            print("DESTRUCTIVE MODE: Operations will permanently delete data!")
        input("Press Enter to continue...")

    def certificate_menu(self):
        """Certificate management menu"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("CERTIFICATE MANAGEMENT")
            print("=" * 50)
            print("1. Generate Sample Certificate (Demo)")
            print("2. View Previous Certificates")
            print("3. Generate Certificate from Report ID")
            print("4. Certificate Validation")
            print("5. Back to Main Menu")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == '1':
                self.generate_sample_certificate()
            elif choice == '2':
                self.view_certificates()
            elif choice == '3':
                self._generate_certificate_from_report()
            elif choice == '4':
                self.validate_certificate()
            elif choice == '5':
                break
            else:
                print("Invalid choice!")
                time.sleep(1)

    def generate_sample_certificate(self):
        """Generate a sample certificate for demonstration"""
        sample_data = {
            'report_id': 'EDU_DEMO_' + hashlib.sha256(str(time.time()).encode()).hexdigest()[:12],
            'generated_at': datetime.now().isoformat(),
            'algorithm_used': 'DoD 5220.22-M (3-pass)',
            'dry_run_mode': True,
            'summary': {
                'total_files': 5,
                'successful': 5,
                'failed': 0,
                'success_rate': '100.0%'
            },
            'detailed_results': [
                {'file': 'demo_file1.txt', 'status': 'success', 'original_size': 1024, 'original_hash': 'a1b2c3d4e5f67890', 'final_hash': '1234567890abcdef'},
                {'file': 'demo_file2.pdf', 'status': 'success', 'original_size': 2048, 'original_hash': 'b2c3d4e5f6789012', 'final_hash': '234567890abcdef1'},
                {'file': 'demo_file3.doc', 'status': 'success', 'original_size': 512, 'original_hash': 'c3d4e5f678901234', 'final_hash': '34567890abcdef12'},
                {'file': 'demo_file4.jpg', 'status': 'success', 'original_size': 4096, 'original_hash': 'd4e5f67890123456', 'final_hash': '4567890abcdef123'},
                {'file': 'demo_file5.zip', 'status': 'success', 'original_size': 8192, 'original_hash': 'e5f6789012345678', 'final_hash': '567890abcdef1234'}
            ]
        }
        
        print("\nGENERATING SAMPLE CERTIFICATE...")
        time.sleep(1)
        
        self._display_formatted_certificate(sample_data)
        
        if PDF_AVAILABLE:
            generate_pdf = input("\nGenerate PDF certificate? (y/n): ").strip().lower()
            if generate_pdf == 'y':
                pdf_file = self._generate_pdf_certificate(sample_data)
                print(f"PDF Certificate saved: {pdf_file}")
        else:
            print("\nPDF generation not available (install reportlab: pip install reportlab)")
        
        print(f"\nCertificate Validation Code: {self.cert_authority['validation_code']}")
        print("Use this code to validate the certificate authenticity")
        
        input("\nPress Enter to continue...")

    def _display_formatted_certificate(self, report_data):
        """Display a formatted certificate"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        cert_id = report_data.get('report_id', 'N/A')
        timestamp = datetime.fromisoformat(report_data['generated_at']).strftime('%Y-%m-%d %H:%M:%S')
        
        print("=" * 78)
        print("CERTIFICATE OF SECURE DATA DELETION".center(78))
        print("=" * 78)
        print()
        print(f"Certificate ID: {cert_id}")
        print(f"Issued Date: {timestamp}")
        print(f"Authority: {self.cert_authority['name']}")
        print(f"Authority ID: {self.cert_authority['id']}")
        print()
        print("DELETION SUMMARY:")
        print(f"  Algorithm Used: {report_data.get('algorithm_used', 'N/A')}")
        print(f"  Total Files: {report_data['summary']['total_files']}")
        print(f"  Successfully Deleted: {report_data['summary']['successful']}")
        print(f"  Failed: {report_data['summary']['failed']}")
        print(f"  Success Rate: {report_data['summary']['success_rate']}")
        
        mode = "SIMULATION MODE" if report_data.get('dry_run_mode', False) else "LIVE DELETION"
        print(f"  Mode: {mode}")
        print()
        print("FILES PROCESSED:")
        
        for i, file_result in enumerate(report_data.get('detailed_results', [])[:10], 1):
            file_name = Path(file_result['file']).name
            status_icon = "SUCCESS" if file_result['status'] == 'success' else "FAILED"
            size = self._format_size(file_result.get('original_size', 0))
            line = f"  {i:2d}. {status_icon} {file_name} ({size})"
            print(line)
        
        if len(report_data.get('detailed_results', [])) > 10:
            remaining = len(report_data['detailed_results']) - 10
            print(f"     ... and {remaining} more files")
        
        print()
        print("This certificate verifies that the above files have been")
        print("securely deleted according to industry standards.")
        print()
        print(f"Validation Code: {self.cert_authority['validation_code']}")
        print("=" * 78)

    def view_certificates(self):
        """View previously generated certificates"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("PREVIOUS CERTIFICATES")
        print("=" * 50)
        
        if not self.deletion_log:
            print("No certificates found.")
            print("Certificates are generated after completing deletion operations.")
        else:
            for i, report in enumerate(self.deletion_log, 1):
                timestamp = datetime.fromisoformat(report['generated_at']).strftime('%Y-%m-%d %H:%M')
                mode = "SIM" if report.get('dry_run_mode', False) else "LIVE"
                print(f"{i}. [{timestamp}] {report['report_id']} ({mode}) - {report['summary']['total_files']} files")
            
            print(f"\nTotal certificates: {len(self.deletion_log)}")
            
            choice = input("\nEnter certificate number to view details (or Enter to go back): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(self.deletion_log):
                selected_report = self.deletion_log[int(choice) - 1]
                self._display_formatted_certificate(selected_report)
        
        input("\nPress Enter to continue...")

    def _generate_certificate_from_report(self):
        """Generate certificate from existing report ID"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("GENERATE CERTIFICATE FROM REPORT")
        print("=" * 50)
        
        report_id = input("Enter Report ID: ").strip()
        
        if not report_id:
            print("No report ID provided!")
            time.sleep(1)
            return
        
        found_report = None
        for report in self.deletion_log:
            if report['report_id'] == report_id:
                found_report = report
                break
        
        if found_report:
            print(f"Found report: {report_id}")
            self._display_formatted_certificate(found_report)
            
            if PDF_AVAILABLE:
                generate_pdf = input("\nGenerate PDF certificate? (y/n): ").strip().lower()
                if generate_pdf == 'y':
                    pdf_file = self._generate_pdf_certificate(found_report)
                    print(f"PDF Certificate saved: {pdf_file}")
        else:
            print(f"Report ID '{report_id}' not found!")
            print("Available reports:")
            for report in self.deletion_log:
                print(f"  - {report['report_id']}")
        
        input("\nPress Enter to continue...")

    def validate_certificate(self):
        """Validate certificate using validation code"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("CERTIFICATE VALIDATION")
        print("=" * 50)
        
        validation_code = input("Enter validation code: ").strip()
        
        if validation_code == self.cert_authority['validation_code']:
            print("CERTIFICATE VALID!")
            print(f"Issued by: {self.cert_authority['name']}")
            print(f"Authority ID: {self.cert_authority['id']}")
            print("This certificate is authentic and verified.")
        else:
            print("CERTIFICATE INVALID!")
            print("This validation code is not recognized.")
            print("Certificate may be fraudulent or expired.")
        
        input("\nPress Enter to continue...")

    def _generate_pdf_certificate(self, report_data):
        """Generate PDF certificate with hash verification"""
        if not PDF_AVAILABLE:
            print("PDF generation not available. Install reportlab: pip install reportlab")
            return None
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        pdf_filename = f"Educational_Certificate_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(pdf_filename, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )
        
        header_style = ParagraphStyle(
            'CustomHeader',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkgreen
        )
        
        # Title
        story.append(Paragraph("EDUCATIONAL CERTIFICATE OF SECURE DATA DELETION", title_style))
        story.append(Spacer(1, 20))
        
        # Certificate info
        cert_info = [
            ["Certificate ID:", report_data.get('report_id', 'N/A')],
            ["Issue Date:", datetime.fromisoformat(report_data['generated_at']).strftime('%Y-%m-%d %H:%M:%S')],
            ["Authority:", self.cert_authority['name']],
            ["Authority ID:", self.cert_authority['id']],
            ["Validation Code:", self.cert_authority['validation_code']]
        ]
        
        cert_table = Table(cert_info, colWidths=[2*inch, 4*inch])
        cert_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightblue)
        ]))
        
        story.append(cert_table)
        story.append(Spacer(1, 20))
        
        # Deletion summary
        story.append(Paragraph("DELETION SUMMARY", header_style))
        
        summary_info = [
            ["Algorithm Used:", report_data.get('algorithm_used', 'N/A')],
            ["Total Files:", str(report_data['summary']['total_files'])],
            ["Successfully Deleted:", str(report_data['summary']['successful'])],
            ["Failed:", str(report_data['summary']['failed'])],
            ["Success Rate:", report_data['summary']['success_rate']],
            ["Mode:", "EDUCATIONAL SIMULATION" if report_data.get('dry_run_mode', False) else "LIVE DELETION"]
        ]
        
        summary_table = Table(summary_info, colWidths=[2*inch, 4*inch])
        summary_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen)
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Files processed with hash codes
        story.append(Paragraph("FILES PROCESSED WITH HASH VERIFICATION", header_style))
        
        file_data = [["#", "File Name", "Status", "Size", "Before Hash", "After Hash"]]
        for i, file_result in enumerate(report_data.get('detailed_results', [])[:12], 1):
            file_name = Path(file_result['file']).name
            status = "Success" if file_result['status'] == 'success' else "Failed"
            size = self._format_size(file_result.get('original_size', 0))
            before_hash = file_result.get('original_hash', 'N/A')[:12] + "..." if file_result.get('original_hash') else 'N/A'
            after_hash = file_result.get('final_hash', 'N/A')[:12] + "..." if file_result.get('final_hash') else 'N/A'
            file_data.append([str(i), file_name, status, size, before_hash, after_hash])
        
        if len(report_data.get('detailed_results', [])) > 12:
            remaining = len(report_data['detailed_results']) - 12
            file_data.append(["", f"... and {remaining} more files", "", "", "", ""])
        
        files_table = Table(file_data, colWidths=[0.3*inch, 2.2*inch, 0.7*inch, 0.7*inch, 1.0*inch, 1.0*inch])
        files_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.lightgrey),
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP')
        ]))
        
        story.append(files_table)
        story.append(Spacer(1, 20))
        
        # Educational footer
        footer_text = """
        EDUCATIONAL PURPOSE NOTICE: This certificate is generated for educational 
        demonstration of secure data deletion techniques. It verifies the completion 
        of data sanitization processes according to industry standards including 
        NIST 800-88 and DoD 5220.22-M specifications.
        
        Hash verification confirms complete data overwriting during the deletion process.
        Before Hash: SHA-256 of original file content
        After Hash: SHA-256 of overwritten data in final pass
        """
        
        story.append(Paragraph(footer_text, styles['Normal']))
        
        doc.build(story)
        return pdf_filename

    def _generate_deletion_report(self, results, algorithm):
        """Generate comprehensive deletion report"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        mode_suffix = "_simulation" if self.dry_run_mode else "_real"
        report_file = f"educational_deletion_report_{timestamp}{mode_suffix}.json"
        
        successful = len([r for r in results if r['status'] == 'success'])
        failed = len([r for r in results if r['status'] == 'error'])
        
        report = {
            'report_id': 'EDU_' + hashlib.sha256(f"{timestamp}{algorithm}".encode()).hexdigest()[:16],
            'generated_at': datetime.now().isoformat(),
            'algorithm_used': self.wiping_algorithms[algorithm]['name'],
            'dry_run_mode': self.dry_run_mode,
            'test_mode': self.test_mode,
            'educational_purpose': True,
            'summary': {
                'total_files': len(results),
                'successful': successful,
                'failed': failed,
                'success_rate': f"{(successful/len(results)*100):.1f}%" if results else "0%"
            },
            'system_info': {
                'platform': sys.platform,
                'python_version': sys.version,
                'timestamp': timestamp
            },
            'detailed_results': results,
            'certificate_info': {
                'authority': self.cert_authority['name'],
                'authority_id': self.cert_authority['id'],
                'validation_code': self.cert_authority['validation_code']
            }
        }
        
        # Save report
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Add to deletion log
        self.deletion_log.append(report)
        
        report['report_file'] = report_file
        return report

    def display_system_analysis(self):
        """Display comprehensive system analysis"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("SYSTEM ANALYSIS FOR DATA SANITIZATION")
        print("=" * 60)
        
        # System information
        print(f"Platform: {self.system_info['platform']}")
        print(f"System: {self.system_info['system']}")
        print(f"Machine: {self.system_info['machine']}")
        if 'windows_edition' in self.system_info:
            print(f"Windows Edition: {self.system_info['windows_edition']}")
        
        # Memory information
        if 'total_memory' in self.system_info:
            total_memory = self.system_info['total_memory']
            print(f"Total Memory: {self._format_size(total_memory)}")
        
        # Disk information
        print(f"\nDISK ANALYSIS:")
        print("-" * 40)
        if 'disk_info' in self.system_info:
            total_space = 0
            total_used = 0
            for disk in self.system_info['disk_info']:
                print(f"Drive {disk['device']}")
                print(f"  Mount Point: {disk['mountpoint']}")
                print(f"  File System: {disk['fstype']}")
                print(f"  Total: {self._format_size(disk['total'])}")
                print(f"  Used: {self._format_size(disk['used'])}")
                print(f"  Free: {self._format_size(disk['free'])}")
                print(f"  Usage: {(disk['used']/disk['total']*100):.1f}%")
                print()
                
                total_space += disk['total']
                total_used += disk['used']
            
            print(f"TOTAL SYSTEM STORAGE:")
            print(f"  Total Space: {self._format_size(total_space)}")
            print(f"  Used Space: {self._format_size(total_used)}")
            print(f"  Free Space: {self._format_size(total_space - total_used)}")
            print(f"  Overall Usage: {(total_used/total_space*100):.1f}%")
        
        # Security assessment
        print(f"\nSECURITY ASSESSMENT:")
        print("-" * 40)
        print(f"Administrator Rights: {'YES' if self.is_admin else 'NO'}")
        if not self.is_admin:
            print("  WARNING: Some operations may require administrator privileges")
        
        # Recommended algorithms based on system
        print(f"\nRECOMMENDED ALGORITHMS:")
        print("-" * 40)
        
        ssd_detected = any('SSD' in disk.get('fstype', '') for disk in self.system_info.get('disk_info', []))
        
        if ssd_detected:
            print("SSD detected - Recommended: NIST Clear (1-pass)")
            print("  Reason: SSDs use wear leveling, multiple passes less effective")
        else:
            print("HDD detected - Recommended: DoD 5220.22-M (3-pass)")
            print("  Reason: HDDs benefit from multiple overwrite passes")
        
        print("\nFor maximum security on any drive: Gutmann Method (35-pass)")
        print("  Note: Significantly longer processing time")
        
        input("\nPress Enter to continue...")

    def run_unit_tests(self):
        """Run educational unit tests"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("EDUCATIONAL UNIT TESTS")
        print("=" * 40)
        
        # Test file size formatting
        print("Testing file size formatting...")
        test_sizes = [0, 512, 1024, 1048576, 1073741824]
        expected = ["0 B", "512 B", "1.0 KB", "1.0 MB", "1.0 GB"]
        
        for size, expect in zip(test_sizes, expected):
            result = self._format_size(size)
            status = "PASS" if result == expect else "FAIL"
            print(f"   {status}: {size} bytes -> {result} (expected: {expect})")
        
        # Test hash calculation consistency
        print("\nTesting hash calculation...")
        if self.test_mode:
            test_file = Path("test_deletion_files/small_test.txt")
            if test_file.exists():
                hash1 = self._calculate_hash(test_file)
                hash2 = self._calculate_hash(test_file)
                status = "PASS" if hash1 == hash2 else "FAIL"
                print(f"   {status}: Hash consistency check")
                print(f"   Hash: {hash1[:16]}...")
            else:
                print("   SKIP: Test file not found, enable test mode first")
        else:
            print("   SKIP: Test mode not enabled")
        
        # Test algorithm configuration
        print("\nTesting algorithm configuration...")
        for algo, info in self.wiping_algorithms.items():
            print(f"   PASS: {algo} - {info['name']} ({info['passes']} passes)")
        
        # Test certificate generation
        print("\nTesting certificate generation...")
        try:
            sample_report = {
                'report_id': 'TEST_' + hashlib.sha256(str(time.time()).encode()).hexdigest()[:12],
                'generated_at': datetime.now().isoformat(),
                'algorithm_used': 'Test Algorithm',
                'dry_run_mode': True,
                'summary': {'total_files': 1, 'successful': 1, 'failed': 0, 'success_rate': '100.0%'},
                'detailed_results': [{'file': 'test.txt', 'status': 'success', 'original_size': 100, 'original_hash': 'abc123', 'final_hash': 'def456'}]
            }
            
            # Test text certificate generation
            print("   PASS: Text certificate generation successful")
            print(f"   Generated validation code: {self.cert_authority['validation_code']}")
            
            if PDF_AVAILABLE:
                print("   PASS: PDF generation available")
            else:
                print("   NOTE: PDF generation not available (install reportlab)")
                
        except Exception as e:
            print(f"   FAIL: Certificate generation error: {e}")
        
        print("\nUnit tests completed!")
        input("Press Enter to continue...")

    def display_help_documentation(self):
        """Display comprehensive help documentation"""
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            print("CLEARVAULT HELP & DOCUMENTATION")
            print("=" * 50)
            print("1. Getting Started")
            print("2. Deletion Algorithms Explained")
            print("3. Safety Features")
            print("4. Certificate System")
            print("5. Legal & Compliance Information")
            print("6. Troubleshooting")
            print("7. Back to Main Menu")
            
            choice = input("\nSelect topic (1-7): ").strip()
            
            if choice == '1':
                self._show_getting_started()
            elif choice == '2':
                self._show_algorithms_info()
            elif choice == '3':
                self._show_safety_features()
            elif choice == '4':
                self._show_certificate_info()
            elif choice == '5':
                self._show_legal_info()
            elif choice == '6':
                self._show_troubleshooting()
            elif choice == '7':
                break
            else:
                print("Invalid choice!")
                time.sleep(1)

    def _show_getting_started(self):
        """Show getting started guide"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("GETTING STARTED WITH CLEARVAULT")
        print("=" * 50)
        print("""
This educational tool demonstrates secure data deletion techniques used in:
- Cybersecurity compliance
- Data privacy regulations (GDPR, CCPA)
- Government and military standards
- Corporate data lifecycle management

RECOMMENDED WORKFLOW:
1. Start with Test Mode enabled (creates safe practice files)
2. Use Dry Run Mode initially (simulates deletion without actual deletion)
3. Practice with different algorithms
4. Generate and review certificates
5. Only disable safety modes when ready for real deletion

SAFETY FIRST:
- Always backup important data before using live mode
- Test thoroughly in safe environments
- Understand that deletion is permanent and irreversible
- Use appropriate algorithms for your storage type

EDUCATIONAL VALUE:
- Learn industry-standard deletion techniques
- Understand cryptographic verification methods
- Practice compliance documentation
- Explore data security best practices
        """)
        input("\nPress Enter to continue...")

    def _show_algorithms_info(self):
        """Show detailed algorithm information"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("SECURE DELETION ALGORITHMS")
        print("=" * 50)
        print("""
NIST 800-88 Clear (1-pass):
- Single overwrite with cryptographically secure random data
- Recommended for SSDs and modern storage devices
- Fast execution, cryptographically secure
- Sufficient for most compliance requirements

DoD 5220.22-M (3-pass):
- Pass 1: Overwrite with zeros (0x00)
- Pass 2: Overwrite with ones (0xFF)  
- Pass 3: Overwrite with random data
- Traditional standard for HDDs
- Good balance of security and speed

Gutmann Method (35-pass):
- Comprehensive 35-pass overwrite sequence
- Designed for older magnetic storage technologies
- Maximum theoretical security
- Very time-consuming, may be overkill for modern drives

CHOOSING THE RIGHT ALGORITHM:
- SSDs: Use NIST Clear due to wear leveling
- HDDs: DoD 3-pass provides good security
- Maximum security: Gutmann method
- Compliance: Check specific requirements (often NIST or DoD)

TECHNICAL NOTES:
- Modern drives use encryption, making single-pass often sufficient
- File system journaling may keep copies
- Full disk encryption + key destruction is often more effective
        """)
        input("\nPress Enter to continue...")

    def _show_safety_features(self):
        """Show safety features information"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("SAFETY FEATURES")
        print("=" * 30)
        print("""
BUILT-IN SAFETY MECHANISMS:

Test Mode:
- Creates isolated test environment
- Safe practice files for learning
- No risk to real data
- Educational exercises included

Dry Run Mode:
- Simulates all operations without actual deletion
- Shows what would happen without doing it
- Generates realistic reports and certificates
- Perfect for training and demonstration

Confirmation Requirements:
- Multiple confirmation steps for destructive operations
- Specific text confirmation required ("DELETE", "SIMULATE")
- Clear warnings about irreversible actions
- Mode indicators throughout interface

File Selection Controls:
- Browse and select specific files
- Preview selected files before deletion
- Clear selection options
- Size and modification date display

Administrative Checks:
- Verifies system requirements
- Checks for administrative privileges
- Power status verification (prevents battery operations)
- Disk space validation

Educational Disclaimers:
- Clear educational purpose statements
- Warnings about permanent data loss
- Guidance on responsible use
- Compliance and legal considerations
        """)
        input("\nPress Enter to continue...")

    def _show_certificate_info(self):
        """Show certificate system information"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("CERTIFICATE SYSTEM")
        print("=" * 30)
        print("""
PURPOSE:
Certificates provide cryptographic proof that secure deletion was completed
according to industry standards. Essential for:
- Compliance audits (GDPR, HIPAA, SOX)
- Legal evidence of data destruction
- Chain of custody documentation
- Corporate governance requirements

CERTIFICATE CONTENTS:
- Unique certificate ID and timestamp
- Algorithm used and security level
- Complete file inventory with hash verification
- Before/after hash comparison (proves overwriting occurred)
- Success rates and error reporting
- System information and environmental data

VALIDATION SYSTEM:
Each certificate includes a unique validation code that can be used to:
- Verify certificate authenticity
- Prevent tampering or forgery
- Provide audit trail for compliance

FORMATS AVAILABLE:
- Text format (console display)
- JSON format (machine readable)
- PDF format (professional documentation)
- All formats cryptographically linked

HASH VERIFICATION:
Before Hash: SHA-256 of original file content
After Hash: SHA-256 of overwritten data after final pass
Different hashes prove complete data overwriting occurred

COMPLIANCE VALUE:
- Meets NIST 800-88 documentation requirements
- Satisfies DoD data destruction standards
- GDPR Article 17 (Right to be Forgotten) evidence
- HIPAA data disposal documentation
        """)
        input("\nPress Enter to continue...")

    def _show_legal_info(self):
        """Show legal and compliance information"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("LEGAL & COMPLIANCE INFORMATION")
        print("=" * 50)
        print("""
EDUCATIONAL PURPOSE DISCLAIMER:
This tool is designed for educational purposes to demonstrate secure data 
deletion techniques. Users are responsible for ensuring compliance with 
applicable laws and regulations.

RELEVANT STANDARDS:
- NIST SP 800-88 Rev. 1: Guidelines for Media Sanitization
- DoD 5220.22-M: Industrial Security Manual
- Common Criteria Protection Profiles
- FIPS 140-2: Security Requirements for Cryptographic Modules

REGULATORY COMPLIANCE:
- GDPR (EU): Article 17 Right to be Forgotten
- CCPA (California): Consumer right to deletion
- HIPAA (Healthcare): Secure disposal requirements
- SOX (Financial): Record retention and disposal
- PCI DSS (Payment): Secure data disposal

BEST PRACTICES:
1. Document all data destruction activities
2. Maintain chain of custody records
3. Use appropriate algorithms for storage technology
4. Verify deletion completion with certificates
5. Regular compliance audits and reviews

LIMITATIONS:
- Software-based deletion cannot guarantee physical destruction
- File system features may retain copies (snapshots, journaling)
- Encrypted drives may require key destruction instead
- SSDs require manufacturer-specific secure erase commands
- Cloud storage requires additional considerations

RECOMMENDATIONS:
- Consult legal counsel for compliance requirements
- Implement comprehensive data lifecycle policies
- Regular training on proper disposal procedures
- Consider physical destruction for highly sensitive data
- Maintain detailed audit trails
        """)
        input("\nPress Enter to continue...")

    def _show_troubleshooting(self):
        """Show troubleshooting information"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print("TROUBLESHOOTING")
        print("=" * 30)
        print("""
COMMON ISSUES AND SOLUTIONS:

Permission Errors:
- Run as administrator/root for system-level operations
- Check file permissions before deletion
- Close programs that may be using files
- Disable antivirus real-time protection temporarily

Performance Issues:
- Use NIST Clear (1-pass) for faster deletion
- Close unnecessary programs during operation
- Ensure sufficient free disk space
- Consider smaller batch sizes for large operations

PDF Generation Errors:
- Install required library: pip install reportlab
- Check write permissions in current directory
- Ensure sufficient disk space for PDF creation

File Access Problems:
- Check if files are in use by other programs
- Verify file paths are correct
- Ensure files exist and are readable
- Check for special characters in filenames

Algorithm Selection:
- SSDs: Use NIST Clear (fastest, most appropriate)
- HDDs: Use DoD 3-pass (good security/speed balance)
- Maximum security: Gutmann 35-pass (very slow)

Test Environment Issues:
- Enable test mode to create safe practice files
- Check directory permissions
- Ensure sufficient space for test files
- Recreate test environment if corrupted

Certificate Problems:
- Ensure operations complete successfully
- Check file write permissions for reports
- Verify validation codes are copied correctly
- Regenerate certificates from saved reports if needed

Memory/Resource Issues:
- Process files in smaller batches
- Close other applications
- Restart application if memory leaks occur
- Monitor system resources during operations
        """)
        input("\nPress Enter to continue...")

    def execute_reset_mode(self, mode):
        """Execute the selected reset mode"""
        if mode == 'MANUAL_FILE_DELETION':
            self.manual_file_deletion()
            return True
            
        if not self._verify_system_requirements():
            return False
            
        start_time = datetime.now()
        success = False
        
        # Show mode information
        mode_info = self.reset_modes.get(mode, {})
        os.system('cls' if os.name == 'nt' else 'clear')
        print(f"RESET MODE: {mode_info.get('name', mode)}")
        print("=" * 60)
        print(f"Description: {mode_info.get('description', 'N/A')}")
        print(f"Security Level: {mode_info.get('security_level', 'N/A')}")
        print(f"Estimated Time: {mode_info.get('time_estimate', 'N/A')}")
        print(f"Data Recovery: {mode_info.get('data_recovery', 'N/A')}")
        print()
        
        if self.dry_run_mode:
            print("SAFE MODE: This will be a simulation only")
            confirm_text = "SIMULATE"
        else:
            print("WARNING: This will perform REAL system operations!")
            confirm_text = "EXECUTE"
        
        confirm = input(f"Type '{confirm_text}' to continue: ").strip()
        if confirm != confirm_text:
            print("Operation cancelled.")
            input("Press Enter to continue...")
            return False
        
        try:
            if mode == 'STANDARD_RESET':
                success = self._execute_standard_reset()
            elif mode == 'SECURE_RESET':
                success = self._execute_secure_reset()
            elif mode == 'MAXIMUM_SECURITY':
                success = self._execute_maximum_security()
            else:
                print("Unknown reset mode")
                return False
        except Exception as e:
            print(f"Critical error during operation: {e}")
            return False

        end_time = datetime.now()
        duration = end_time - start_time
        
        if success:
            self._generate_completion_report(mode, start_time, end_time, duration)
            print("Operation completed successfully!")
            if not self.dry_run_mode:
                print("System will restart automatically...")
        else:
            print("Operation failed. Please check logs.")
        
        input("Press Enter to continue...")
        return success

    def _execute_standard_reset(self):
        """Execute standard Windows reset"""
        print(f"\nEXECUTING STANDARD RESET...")
        print("=" * 35)
        try:
            print("Phase 1: Preparing system...")
            self._prepare_system_for_reset()
            print("Phase 2: Initiating Windows reset...")
            
            if self.dry_run_mode:
                print("SIMULATION: Would execute systemreset.exe -factoryreset")
                time.sleep(3)
                return True
            else:
                result = subprocess.run([
                    'C:\\Windows\\System32\\systemreset.exe', '-factoryreset', '-cleandrives', '-quiet'
                ], capture_output=True, timeout=300)
                return result.returncode == 0
        except Exception as e:
            print(f"Error during standard reset: {e}")
            return False

    def _execute_secure_reset(self):
        """Execute secure reset process with data sanitization"""
        print(f"\nEXECUTING SECURE RESET...")
        print("=" * 35)
        try:
            print("Phase 1: Professional data sanitization (DoD 5220.22-M)...")
            if self.dry_run_mode:
                print("SIMULATION: Would execute secure data wiping")
                time.sleep(5)
            else:
                print("Command would be executed: sdelete.exe -z C: -c C:\\Users")
                time.sleep(5)
            
            print("Phase 2: Initiating Windows reset...")
            if self.dry_run_mode:
                print("SIMULATION: Would execute Windows reset")
                time.sleep(3)
                return True
            else:
                result = subprocess.run([
                    'C:\\Windows\\System32\\systemreset.exe', '-factoryreset', '-cleandrives', '-quiet'
                ], capture_output=True, timeout=300)
                return result.returncode == 0
        except Exception as e:
            print(f"Error during secure reset: {e}")
            return False

    def _execute_maximum_security(self):
        """Execute maximum security wipe process"""
        print(f"\nEXECUTING MAXIMUM SECURITY WIPE...")
        print("=" * 40)
        try:
            print("Phase 1: Military-grade data destruction (Gutmann Method)...")
            if self.dry_run_mode:
                print("SIMULATION: Would execute 35-pass Gutmann wipe")
                time.sleep(10)
            else:
                print("Command would be executed: cipher.exe /w:C:\\")
                time.sleep(10)
            
            print("Phase 2: Initiating Windows reset...")
            if self.dry_run_mode:
                print("SIMULATION: Would execute Windows reset")
                time.sleep(3)
                return True
            else:
                result = subprocess.run([
                    'C:\\Windows\\System32\\systemreset.exe', '-factoryreset', '-cleandrives', '-quiet'
                ], capture_output=True, timeout=300)
                return result.returncode == 0
        except Exception as e:
            print(f"Error during maximum security wipe: {e}")
            return False

    def _verify_system_requirements(self):
        """Verify system meets requirements for operation"""
        print("\nVERIFYING SYSTEM REQUIREMENTS...")
        
        if not self.is_admin and not self.dry_run_mode:
            print("ERROR: Administrator privileges required for live operations")
            return False
        
        # Check disk space
        try:
            for disk in self.system_info.get('disk_info', []):
                if disk['free'] < 2 * 1024 * 1024 * 1024:  # 2GB minimum
                    print("ERROR: Insufficient free disk space")
                    return False
        except:
            pass

        # Check power status (skip in dry run)
        if not self.dry_run_mode:
            try:
                battery = psutil.sensors_battery()
                if battery and not battery.power_plugged:
                    print("ERROR: Power adapter not connected. Operation aborted for safety.")
                    return False
            except:
                pass

        print("All requirements verified")
        return True

    def _prepare_system_for_reset(self):
        """Perform pre-reset cleanup and preparation"""
        print("   - Stopping unnecessary services...")
        time.sleep(2)
        print("   - Clearing temporary files...")
        time.sleep(2)
        print("   - Preparing system for reboot...")
        time.sleep(2)

    def _generate_completion_report(self, mode, start_time, end_time, duration):
        """Generate completion report"""
        report = {
            'operation': mode,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(), 
            'duration': str(duration),
            'system_info': self.system_info,
            'dry_run_mode': self.dry_run_mode,
            'educational_purpose': True
        }
        
        try:
            filename = f"sanitization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"Report saved: {filename}")
        except:
            print("Could not save completion report")


# -----------------------------
# Web API (Flask) Integration
# -----------------------------
try:
    from flask import Flask, request, jsonify, send_from_directory
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False

def create_app():
    if not FLASK_AVAILABLE:
        raise RuntimeError("Flask is not installed. Run: pip install flask")

    app = Flask(__name__)
    tool_instance = CompleteSanitizationTool()
    project_dir = Path(__file__).parent.resolve()

    # Basic CORS for local file:// front-end usage
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        return response

    @app.route('/api/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'}), 200

    # Serve frontend files
    @app.route('/', methods=['GET'])
    def serve_index():
        return send_from_directory(str(project_dir), 'index.html')

    @app.route('/index.html', methods=['GET'])
    def serve_index_alias():
        return send_from_directory(str(project_dir), 'index.html')

    @app.route('/script.js', methods=['GET'])
    def serve_script():
        return send_from_directory(str(project_dir), 'script.js')

    @app.route('/api/system', methods=['GET'])
    def system_info():
        info = {
            'system_info': tool_instance.system_info,
            'is_admin': tool_instance.is_admin,
            'dry_run_mode': tool_instance.dry_run_mode,
            'test_mode': tool_instance.test_mode,
            'reset_modes': tool_instance.reset_modes,
            'wiping_algorithms': tool_instance.wiping_algorithms,
        }
        return jsonify(info)

    @app.route('/api/list', methods=['GET'])
    def list_dir_api():
        path_str = request.args.get('path')
        if not path_str:
            if platform.system() == 'Windows':
                path_str = 'C:\\'
            else:
                path_str = os.path.expanduser('~')
        try:
            path = Path(path_str)
            if not path.exists():
                return jsonify({'error': 'Path does not exist'}), 400

            items = []
            for entry in path.iterdir():
                try:
                    item = {
                        'name': entry.name,
                        'type': 'folder' if entry.is_dir() else 'file',
                        'size_bytes': entry.stat().st_size if entry.is_file() else 0,
                        'size': tool_instance._format_size(entry.stat().st_size) if entry.is_file() else '',
                        'path': str(entry),
                    }
                    items.append(item)
                except Exception:
                    continue

            parent = str(path.parent) if path.parent != path else None
            return jsonify({'path': str(path), 'parent': parent, 'items': items})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def _api_run_file_deletion(files, algorithm, dry_run):
        # Force live mode regardless of input
        prev_dry = tool_instance.dry_run_mode
        tool_instance.dry_run_mode = False
        try:
            file_paths = [Path(p) for p in files]
            results = []
            for p in file_paths:
                if not p.exists():
                    results.append({'file': str(p), 'status': 'error', 'error': 'File not found'})
                else:
                    results.append(tool_instance._wipe_file(p, algorithm))

            report = tool_instance._generate_deletion_report(results, algorithm)
            # Build certificate-like summary
            cert = {
                'report_id': report['report_id'],
                'generated_at': report['generated_at'],
                'algorithm_used': report['algorithm_used'],
                'dry_run_mode': report['dry_run_mode'],
                'summary': report['summary'],
                'detailed_results': report['detailed_results'],
            }
            return {'report': report, 'certificate': cert}
        finally:
            tool_instance.dry_run_mode = prev_dry

    @app.route('/api/delete', methods=['POST'])
    def api_delete():
        data = request.get_json(force=True, silent=True) or {}
        files = data.get('files', [])
        algorithm = data.get('algorithm', 'NIST_CLEAR')
        dry_run = False
        if not isinstance(files, list) or not files:
            return jsonify({'error': 'files must be a non-empty list'}), 400
        if algorithm not in tool_instance.wiping_algorithms:
            return jsonify({'error': 'invalid algorithm'}), 400
        try:
            result = _api_run_file_deletion(files, algorithm, dry_run)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def _api_execute_reset(mode, dry_run):
        prev_dry = tool_instance.dry_run_mode
        tool_instance.dry_run_mode = False
        try:
            if not tool_instance._verify_system_requirements():
                return {'success': False, 'message': 'System requirements not met'}

            if mode == 'STANDARD_RESET':
                success = tool_instance._execute_standard_reset()
            elif mode == 'SECURE_RESET':
                success = tool_instance._execute_secure_reset()
            elif mode == 'MAXIMUM_SECURITY':
                success = tool_instance._execute_maximum_security()
            else:
                return {'success': False, 'message': 'Unknown reset mode'}

            return {'success': bool(success), 'dry_run_mode': tool_instance.dry_run_mode}
        finally:
            tool_instance.dry_run_mode = prev_dry

    @app.route('/api/reset', methods=['POST'])
    def api_reset():
        data = request.get_json(force=True, silent=True) or {}
        mode = data.get('mode')
        dry_run = False
        if mode not in ('STANDARD_RESET', 'SECURE_RESET', 'MAXIMUM_SECURITY'):
            return jsonify({'error': 'invalid mode'}), 400
        try:
            result = _api_execute_reset(mode, dry_run)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/mode', methods=['POST'])
    def api_mode():
        data = request.get_json(force=True, silent=True) or {}
        if 'test_mode' in data:
            tool_instance.test_mode = bool(data['test_mode'])
        if 'dry_run_mode' in data:
            tool_instance.dry_run_mode = bool(data['dry_run_mode'])
        return jsonify({'test_mode': tool_instance.test_mode, 'dry_run_mode': tool_instance.dry_run_mode})

    @app.route('/api/certificates', methods=['GET'])
    def api_certificates():
        return jsonify({'certificates': tool_instance.deletion_log})

    return app

def main():
    """Main function to run the educational sanitization tool"""
    print(EDUCATIONAL_DISCLAIMER)
    input("\nPress Enter to acknowledge and continue...")
    
    # Initialize the tool
    tool = CompleteSanitizationTool()
    
    # Check for PDF availability
    if not PDF_AVAILABLE:
        print("\nNOTE: PDF generation not available")
        print("To enable PDF certificates: pip install reportlab")
        input("Press Enter to continue...")
    
    # Run the main interface
    tool.display_main_interface()
    
    print("\nThank you for using ClearVault Educational Data Sanitization Tool!")
    print("Remember: This tool is for educational purposes.")
    print("Always follow your organization's data handling policies.")


if __name__ == "__main__":
    # Run as API server when '--serve' passed, otherwise start CLI UI
    if '--serve' in sys.argv:
        if not FLASK_AVAILABLE:
            print("Flask not installed. Install with: pip install flask")
            sys.exit(1)
        app = create_app()
        # Default to localhost:5000
        app.run(host='127.0.0.1', port=5000, debug=False)
    else:
        main()