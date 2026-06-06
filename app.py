from flask import Flask, render_template, request, jsonify, send_file, session
import os
import sys
import json
import threading
from pathlib import Path
from datetime import timedelta

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the backend
from backend import CompleteSanitizationTool, PDF_AVAILABLE

app = Flask(__name__)
app.secret_key = 'clearvault-secret-key-2024'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=2)

# Global instance of the sanitization tool
sanitization_tool = CompleteSanitizationTool()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/system_info', methods=['GET'])
def get_system_info():
    try:
        # Get system info from backend
        system_info = sanitization_tool.system_info
        
        # Format disk info for frontend
        disk_info = []
        if 'disk_info' in system_info:
            for disk in system_info['disk_info']:
                disk_info.append({
                    'device': disk['device'],
                    'mountpoint': disk['mountpoint'],
                    'total': disk['total'],
                    'used': disk['used'],
                    'free': disk['free']
                })
        
        return jsonify({
            'success': True,
            'platform': system_info.get('platform', 'Unknown'),
            'system': system_info.get('system', 'Unknown'),
            'release': system_info.get('release', 'Unknown'),
            'machine': system_info.get('machine', 'Unknown'),
            'windows_edition': system_info.get('windows_edition', 'Unknown'),
            'disk_info': disk_info
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/list_directory', methods=['POST'])
def list_directory():
    try:
        data = request.json
        path = data.get('path', '')
        
        if not path:
            if os.name == 'nt':
                path = "C:\\"
            else:
                path = os.path.expanduser("~")
        
        current_path = Path(path)
        items = []
        
        # Add parent directory if not root
        if current_path.parent != current_path:
            items.append({
                'name': '..',
                'type': 'parent',
                'path': str(current_path.parent),
                'size': '0 B'
            })
        
        # Get directory contents
        for item in current_path.iterdir():
            try:
                if item.is_dir():
                    items.append({
                        'name': item.name,
                        'type': 'folder',
                        'path': str(item),
                        'size': '0 B'
                    })
                else:
                    size = item.stat().st_size
                    size_str = sanitization_tool._format_size(size)
                    items.append({
                        'name': item.name,
                        'type': 'file',
                        'path': str(item),
                        'size': size_str
                    })
            except (PermissionError, OSError) as e:
                items.append({
                    'name': item.name,
                    'type': 'file',
                    'path': str(item),
                    'size': 'Permission Denied',
                    'error': True
                })
                continue
        
        return jsonify({
            'success': True,
            'path': str(current_path),
            'items': items
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/select_files', methods=['POST'])
def select_files():
    try:
        data = request.json
        file_paths = data.get('files', [])
        
        # Store selected files in session
        session['selected_files'] = file_paths
        
        # Calculate total size
        total_size = 0
        valid_files = []
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    size = os.path.getsize(file_path)
                    total_size += size
                    valid_files.append(file_path)
                except OSError:
                    continue
        
        session['selected_files'] = valid_files
        
        return jsonify({
            'success': True,
            'selected_count': len(valid_files),
            'total_size': sanitization_tool._format_size(total_size),
            'selected_files': valid_files
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/delete_files', methods=['POST'])
def delete_files():
    try:
        data = request.json
        file_paths = data.get('files', [])
        algorithm = data.get('algorithm', 'NIST_CLEAR')
        
        # Convert to Path objects
        file_objects = [Path(fp) for fp in file_paths if os.path.exists(fp)]
        
        if not file_objects:
            return jsonify({
                'success': False,
                'error': 'No valid files selected'
            })
        
        # Execute secure deletion
        results = []
        for file_path in file_objects:
            try:
                result = sanitization_tool._wipe_file(file_path, algorithm)
                results.append(result)
            except Exception as e:
                results.append({
                    'file': str(file_path),
                    'status': 'error',
                    'error': str(e)
                })
        
        # Generate report
        report = sanitization_tool._generate_deletion_report(results, algorithm)
        
        # Clear selected files after deletion
        session.pop('selected_files', None)
        
        return jsonify({
            'success': True,
            'results': results,
            'report': report
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/execute_reset', methods=['POST'])
def execute_reset():
    try:
        data = request.json
        mode = data.get('mode', 'STANDARD_RESET')
        
        # Map frontend modes to backend modes
        mode_mapping = {
            'standard': 'STANDARD_RESET',
            'professional': 'SECURE_RESET', 
            'enterprise': 'MAXIMUM_SECURITY'
        }
        
        backend_mode = mode_mapping.get(mode, 'STANDARD_RESET')
        
        # Execute the reset mode in a thread to avoid blocking
        def run_reset():
            sanitization_tool.execute_reset_mode(backend_mode)
        
        thread = threading.Thread(target=run_reset)
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'mode': mode,
            'message': 'Reset process started in background'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/generate_certificate', methods=['POST'])
def generate_certificate():
    try:
        data = request.json
        report_data = data.get('report_data', {})
        
        # Generate PDF certificate if available
        pdf_file = None
        if PDF_AVAILABLE and report_data:
            pdf_file = sanitization_tool._generate_pdf_certificate(report_data)
        
        return jsonify({
            'success': True,
            'pdf_file': pdf_file,
            'validation_code': sanitization_tool.cert_authority['validation_code']
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/api/download_certificate/<filename>')
def download_certificate(filename):
    try:
        # Basic security check
        if '..' in filename or filename.startswith('/'):
            return jsonify({'success': False, 'error': 'Invalid filename'})
            
        return send_file(filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'success': False, 'error': 'File not found'})

@app.route('/api/get_settings', methods=['GET'])
def get_settings():
    try:
        return jsonify({
            'success': True,
            'dry_run_mode': sanitization_tool.dry_run_mode,
            'test_mode': sanitization_tool.test_mode,
            'is_admin': sanitization_tool.is_admin
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/toggle_mode', methods=['POST'])
def toggle_mode():
    try:
        data = request.json
        mode_type = data.get('mode_type')
        
        if mode_type == 'test':
            sanitization_tool.toggle_test_mode()
            return jsonify({
                'success': True,
                'test_mode': sanitization_tool.test_mode
            })
        elif mode_type == 'dry_run':
            sanitization_tool.toggle_dry_run_mode()
            return jsonify({
                'success': True,
                'dry_run_mode': sanitization_tool.dry_run_mode
            })
        
        return jsonify({'success': False, 'error': 'Invalid mode type'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
