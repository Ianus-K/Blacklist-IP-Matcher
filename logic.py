import pandas as pd
import os

class IPProcessor:
    @staticmethod
    def read_file(file_path):
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.csv':
            return pd.read_csv(file_path)
        elif ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"ไม่รองรับไฟล์นามสกุล {ext}")

    @staticmethod
    def compare_ips(file_path, blacklist_set):
        df = IPProcessor.read_file(file_path)
        target_col = None
        for col in df.columns:
            if 'ip' in str(col).lower():
                target_col = col
                break
        
        if target_col is None:
            raise ValueError("ไม่พบคอลัมน์ที่มีชื่อว่า 'IP' ในไฟล์")

        # เปรียบเทียบ
        matched = df[df[target_col].astype(str).str.strip().isin(blacklist_set)]
        not_found = df[~df[target_col].astype(str).str.strip().isin(blacklist_set)]
        
        return matched, not_found

    @staticmethod
    def save_to_excel(matched_df, not_found_df, output_path):
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            matched_df.to_excel(writer, sheet_name='Matched IP', index=False)
            not_found_df.to_excel(writer, sheet_name='Not Found IP', index=False)