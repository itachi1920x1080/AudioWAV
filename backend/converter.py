from pydub import AudioSegment
import os

def convert_to_wav(input_path, output_path): # ដូរឈ្មោះមុខងារបន្តិចឲ្យសមន័យ
    """
    បម្លែងឯកសារសំឡេងផ្សេងៗ (MP3, OGG...) ទៅជា WAV
    """
    try:
        print(f"កំពុងអានឯកសារ: {input_path}...")
        
        # ⚠️ ចំណុចផ្លាស់ប្តូរ៖ ប្រើ from_file ដើម្បីស្គាល់គ្រប់ទម្រង់
        audio = AudioSegment.from_file(input_path)
        
        print(f"កំពុងបម្លែង និងរក្សាទុកទៅជា: {output_path}...")
        audio.export(output_path, format="wav")
        
        print("✅ ការបម្លែងទទួលបានជោគជ័យ!")
        return True
        
    except Exception as e:
        print(f"❌ មានបញ្ហាក្នុងការបម្លែង: {e}")
        return False

# # កូដសម្រាប់សាកល្បង (ដំណើរការតែពេលអ្នក Run ឯកសារនេះផ្ទាល់)
# if __name__ == "__main__":
#     # អ្នកអាចបង្កើតឯកសារ test.mp3 មួយសម្រាប់សាកល្បងកូដនេះបាន
#     input_file = "test.mp3"
#     output_file = "test_output.wav"
    
#     if os.path.exists(input_file):
#         convert_mp3_to_wav(input_file, output_file)
#     else:
#         print(f"រកមិនឃើញឯកសារ {input_file} ទេ។ សូមដាក់ឯកសារ mp3 មួយនៅទីនេះដើម្បីសាកល្បង។")