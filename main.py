#!/usr/bin/env python3
"""
文書分類・リネームシステム
OCR機能を備えた汎用文書分類・リネームシステム
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from pathlib import Path
from typing import List, Dict, Optional
import sys

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.pdf_processor import PDFProcessor
from core.ocr_engine import OCREngine
from core.csv_processor import CSVProcessor
from core.classifier import DocumentClassifier
from ui.drag_drop import DropZoneFrame


class DocumentClassifierApp:
    """文書分類・リネームシステムのメインアプリケーションクラス"""
    
    def __init__(self):
        """アプリケーションの初期化"""
        self.root = tk.Tk()
        self.root.title("文書分類・リネームシステム")
        self.root.geometry("1000x700")
        
        # Initialize core components
        self.pdf_processor = PDFProcessor()
        self.ocr_engine = OCREngine()
        self.csv_processor = CSVProcessor()
        self.classifier = DocumentClassifier()
        
        # UI variables
        self.files_list = []
        self.processing = False
        
        # Create UI
        self._create_ui()

    def _create_ui(self):
        """Create the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # タイトル
        title_label = ttk.Label(
            main_frame, 
            text="文書分類・リネームシステム", 
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # 説明
        desc_label = ttk.Label(
            main_frame,
            text="OCRとインテリジェントルールを使用して文書を自動分類・リネームします",
            font=('Arial', 10),
            foreground='gray'
        )
        desc_label.pack(pady=(0, 15))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # タブ1: ファイル処理
        self.process_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.process_frame, text="📁 ファイル処理")
        self._create_process_tab()
        
        # タブ2: 結果
        self.result_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.result_frame, text="📊 結果")
        self._create_result_tab()
        
        # タブ3: ログ
        self.log_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.log_frame, text="📋 ログ")
        self._create_log_tab()

    def _create_process_tab(self):
        """Create the file processing tab"""
        # Create left and right panels
        paned = ttk.PanedWindow(self.process_frame, orient='horizontal')
        paned.pack(fill='both', expand=True)
        
        # Left panel: File selection
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=2)
        
        ttk.Label(left_frame, text="ファイル選択", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Drag and drop zone
        self.drop_zone = DropZoneFrame(left_frame, self._on_files_dropped)
        self.drop_zone.pack(fill='both', expand=True, pady=(0, 10))
        
        # File operation buttons
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Button(button_frame, text="📁 ファイル追加", command=self._select_files).pack(side='left', padx=(0, 5))
        ttk.Button(button_frame, text="📂 フォルダ追加", command=self._select_folder).pack(side='left', padx=5)
        ttk.Button(button_frame, text="🗑️ クリア", command=self._clear_files).pack(side='left', padx=5)
        
        # File list
        ttk.Label(left_frame, text="選択されたファイル:").pack(anchor='w')
        
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill='both', expand=True)
        
        self.files_listbox = tk.Listbox(list_frame)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.files_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Right panel: Settings
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="設定", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # 出力設定
        output_frame = ttk.LabelFrame(right_frame, text="出力設定")
        output_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(output_frame, text="日付形式:").pack(anchor='w')
        self.date_format_var = tk.StringVar(value="YYYY")
        date_combo = ttk.Combobox(
            output_frame, 
            textvariable=self.date_format_var,
            values=["YYYY", "YYMM", "YYYYMM", "YYYYMMDD"],
            state='readonly'
        )
        date_combo.pack(anchor='w', pady=5)
        
        ttk.Label(output_frame, text="カスタム日付（任意）:").pack(anchor='w')
        self.custom_date_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.custom_date_var, width=15).pack(anchor='w', pady=5)
        
        # 処理オプション
        options_frame = ttk.LabelFrame(right_frame, text="処理オプション")
        options_frame.pack(fill='x', pady=(0, 10))
        
        self.enable_ocr_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="OCRを有効にする", variable=self.enable_ocr_var).pack(anchor='w')
        
        self.auto_split_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(options_frame, text="複数ページPDFを自動分割", variable=self.auto_split_var).pack(anchor='w')
        
        # Process button
        process_button_frame = ttk.Frame(right_frame)
        process_button_frame.pack(fill='x', pady=20)
        
        self.process_button = ttk.Button(
            process_button_frame, 
            text="🚀 分類・リネーム実行", 
            command=self._start_processing,
            style='Accent.TButton'
        )
        self.process_button.pack(fill='x', pady=(0, 10))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            process_button_frame, 
            variable=self.progress_var, 
            maximum=100
        )
        self.progress_bar.pack(fill='x', pady=(0, 5))
        
        # ステータスラベル
        self.status_var = tk.StringVar(value="文書処理の準備完了")
        ttk.Label(process_button_frame, textvariable=self.status_var).pack()

    def _create_result_tab(self):
        """Create the results tab"""
        ttk.Label(self.result_frame, text="処理結果", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Results table
        tree_frame = ttk.Frame(self.result_frame)
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('元ファイル名', '新ファイル名', '文書タイプ', '信頼度', 'ステータス')
        self.result_tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        for col in columns:
            self.result_tree.heading(col, text=col)
            if col == '信頼度':
                self.result_tree.column(col, width=100)
            elif col == 'ステータス':
                self.result_tree.column(col, width=120)
            else:
                self.result_tree.column(col, width=200)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.result_tree.pack(side='left', fill='both', expand=True)
        tree_scrollbar.pack(side='right', fill='y')
        
        # Result buttons
        result_button_frame = ttk.Frame(self.result_frame)
        result_button_frame.pack(fill='x', pady=10)
        
        ttk.Button(result_button_frame, text="📁 出力フォルダを開く", command=self._open_output_folder).pack(side='left', padx=(0, 5))
        ttk.Button(result_button_frame, text="💾 結果をエクスポート", command=self._export_results).pack(side='left', padx=5)
        ttk.Button(result_button_frame, text="🔄 結果をクリア", command=self._clear_results).pack(side='left', padx=5)

    def _create_log_tab(self):
        """Create the logs tab"""
        ttk.Label(self.log_frame, text="処理ログ", font=('Arial', 12, 'bold')).pack(pady=(0, 10))
        
        # Log text area
        log_text_frame = ttk.Frame(self.log_frame)
        log_text_frame.pack(fill='both', expand=True)
        
        self.log_text = tk.Text(log_text_frame, wrap='word', font=('Consolas', 9))
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side='left', fill='both', expand=True)
        log_scrollbar.pack(side='right', fill='y')
        
        # Log buttons
        log_button_frame = ttk.Frame(self.log_frame)
        log_button_frame.pack(fill='x', pady=10)
        
        ttk.Button(log_button_frame, text="🗑️ ログクリア", command=self._clear_log).pack(side='left', padx=(0, 5))
        ttk.Button(log_button_frame, text="💾 ログ保存", command=self._save_log).pack(side='left', padx=5)

    def _on_files_dropped(self, files: List[str]):
        """Handle dropped files"""
        for file_path in files:
            if file_path not in self.files_list:
                self.files_list.append(file_path)
                self.files_listbox.insert(tk.END, os.path.basename(file_path))
        
        self._log(f"Added {len(files)} file(s)")

    def _select_files(self):
        """Open file selection dialog"""
        filetypes = [
            ('Supported Files', '*.pdf;*.csv'),
            ('PDF Files', '*.pdf'),
            ('CSV Files', '*.csv'),
            ('All Files', '*.*')
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Documents to Process",
            filetypes=filetypes
        )
        
        if files:
            self._on_files_dropped(list(files))

    def _select_folder(self):
        """Open folder selection dialog"""
        folder = filedialog.askdirectory(title="Select Folder Containing Documents")
        if folder:
            files = []
            for ext in ['.pdf', '.csv']:
                files.extend(Path(folder).glob(f"**/*{ext}"))
            
            if files:
                self._on_files_dropped([str(f) for f in files])
                self._log(f"Found {len(files)} files in folder")
            else:
                messagebox.showinfo("Info", "No supported files found in the selected folder")

    def _clear_files(self):
        """Clear the file list"""
        self.files_list.clear()
        self.files_listbox.delete(0, tk.END)
        self._log("Cleared file list")

    def _start_processing(self):
        """Start the document processing"""
        if not self.files_list:
            messagebox.showwarning("Warning", "Please select files to process")
            return
        
        if self.processing:
            messagebox.showwarning("Warning", "Processing is already in progress")
            return
        
        # Select output folder
        output_folder = filedialog.askdirectory(title="Select Output Folder")
        if not output_folder:
            return
        
        # Start background processing
        self.processing = True
        self._update_ui_state()
        
        thread = threading.Thread(
            target=self._process_files_background,
            args=(output_folder,),
            daemon=True
        )
        thread.start()

    def _process_files_background(self, output_folder: str):
        """Background file processing"""
        try:
            total_files = len(self.files_list)
            processed = 0
            
            for i, file_path in enumerate(self.files_list):
                # Update progress
                progress = (i / total_files) * 100
                filename = os.path.basename(file_path)
                
                self.root.after(0, lambda p=progress: self.progress_var.set(p))
                self.root.after(0, lambda f=filename: self.status_var.set(f"Processing: {f}"))
                
                try:
                    self._process_single_file(file_path, output_folder)
                    processed += 1
                except Exception as e:
                    self._log(f"Error processing {filename}: {str(e)}")
                    self.root.after(0, lambda f=filename, e=str(e): self._add_result_error(f, e))
            
            # Processing complete
            self.root.after(0, lambda: self.progress_var.set(100))
            self.root.after(0, lambda p=processed, t=total_files: self.status_var.set(f"Complete: {p}/{t} files processed"))
            
        except Exception as e:
            self._log(f"Processing error: {str(e)}")
        finally:
            self.root.after(0, self._processing_finished)

    def _process_single_file(self, file_path: str, output_folder: str):
        """Process a single file"""
        filename = os.path.basename(file_path)
        ext = os.path.splitext(file_path)[1].lower()
        
        self._log(f"Processing: {filename}")
        
        if ext == '.pdf':
            self._process_pdf_file(file_path, output_folder)
        elif ext == '.csv':
            self._process_csv_file(file_path, output_folder)
        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _process_pdf_file(self, file_path: str, output_folder: str):
        """Process a PDF file"""
        filename = os.path.basename(file_path)
        
        # Extract text using OCR if enabled
        text = ""
        if self.enable_ocr_var.get():
            try:
                text = self.ocr_engine.extract_text_from_pdf(file_path)
            except Exception as e:
                self._log(f"OCR failed for {filename}: {str(e)}")
        
        # Classify document
        classification_result = self.classifier.classify_document(text, filename)
        
        # Generate new filename
        date_str = self._get_date_string()
        new_filename = f"{classification_result.code}_{classification_result.name}_{date_str}.pdf"
        
        # Copy file to output folder
        import shutil
        output_path = os.path.join(output_folder, new_filename)
        output_path = self._get_unique_filename(output_path)
        shutil.copy2(file_path, output_path)
        
        self._log(f"Completed: {filename} -> {os.path.basename(output_path)}")
        
        # Add result
        self.root.after(0, lambda: self._add_result_success(
            filename,
            os.path.basename(output_path),
            classification_result.name,
            f"{classification_result.confidence:.2f}"
        ))

    def _process_csv_file(self, file_path: str, output_folder: str):
        """Process a CSV file"""
        filename = os.path.basename(file_path)
        
        # Simple CSV classification based on filename and headers
        classification_result = self.classifier.classify_csv_file(file_path)
        
        # Generate new filename
        date_str = self._get_date_string()
        new_filename = f"{classification_result.code}_{classification_result.name}_{date_str}.csv"
        
        # Copy file to output folder
        import shutil
        output_path = os.path.join(output_folder, new_filename)
        output_path = self._get_unique_filename(output_path)
        shutil.copy2(file_path, output_path)
        
        self._log(f"Completed: {filename} -> {os.path.basename(output_path)}")
        
        # Add result
        self.root.after(0, lambda: self._add_result_success(
            filename,
            os.path.basename(output_path),
            classification_result.name,
            f"{classification_result.confidence:.2f}"
        ))

    def _get_date_string(self) -> str:
        """Get formatted date string"""
        if self.custom_date_var.get():
            return self.custom_date_var.get()
        
        import datetime
        now = datetime.datetime.now()
        
        format_type = self.date_format_var.get()
        if format_type == "YYYY":
            return str(now.year)
        elif format_type == "YYMM":
            return f"{now.year % 100:02d}{now.month:02d}"
        elif format_type == "YYYYMM":
            return f"{now.year}{now.month:02d}"
        elif format_type == "YYYYMMDD":
            return f"{now.year}{now.month:02d}{now.day:02d}"
        else:
            return str(now.year)

    def _get_unique_filename(self, filepath: str) -> str:
        """Generate a unique filename if file already exists"""
        if not os.path.exists(filepath):
            return filepath
        
        base, ext = os.path.splitext(filepath)
        counter = 1
        
        while True:
            new_path = f"{base}_{counter:03d}{ext}"
            if not os.path.exists(new_path):
                return new_path
            counter += 1

    def _update_ui_state(self):
        """Update UI state based on processing status"""
        if self.processing:
            self.process_button.config(state='disabled', text="Processing...")
        else:
            self.process_button.config(state='normal', text="🚀 Classify & Rename Files")

    def _processing_finished(self):
        """Handle processing completion"""
        self.processing = False
        self._update_ui_state()
        self.notebook.select(1)  # Switch to results tab
        messagebox.showinfo("Complete", "Document processing completed!")

    def _add_result_success(self, original: str, new_name: str, doc_type: str, confidence: str):
        """Add successful result to results table"""
        self.result_tree.insert('', 'end', values=(
            original, new_name, doc_type, confidence, "✅ Success"
        ))

    def _add_result_error(self, filename: str, error: str):
        """Add error result to results table"""
        self.result_tree.insert('', 'end', values=(
            filename, "-", "-", "-", f"❌ Error: {error}"
        ))

    def _open_output_folder(self):
        """Open the output folder"""
        # This would open the last used output folder
        pass

    def _export_results(self):
        """Export results to CSV"""
        # Implementation for exporting results
        pass

    def _clear_results(self):
        """Clear the results table"""
        for item in self.result_tree.get_children():
            self.result_tree.delete(item)

    def _log(self, message: str):
        """Add message to log"""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.root.after(0, lambda: self.log_text.insert(tk.END, log_entry))
        self.root.after(0, lambda: self.log_text.see(tk.END))

    def _clear_log(self):
        """Clear the log"""
        self.log_text.delete(1.0, tk.END)

    def _save_log(self):
        """Save log to file"""
        # Implementation for saving logs
        pass

    def run(self):
        """Start the application"""
        self._log("Document Classifier & Renamer started")
        self.root.mainloop()


if __name__ == "__main__":
    app = DocumentClassifierApp()
    app.run()