import os

def extract_java_code_from_directory(directory_path):
    all_code = ""
    
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".java"):
                with open(os.path.join(root, file), 'r' , encoding = 'utf-8') as f:
                    all_code += f.read() + "\n\n"
    
    return all_code

def save_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

# Example usage:
# directory_path = "/path/to/your/java/files"
# code = extract_java_code_from_directory(directory_path)

# output_file = "/path/to/your/output/file.txt"
# save_to_file(code, output_file)

directory_path = "C:/Github/HandyBus/src/main/java/HandyBus/HandyBus"

code = extract_java_code_from_directory(directory_path)

output_files = "C:/Github/HandyBus/extractcode/output.txt"
save_to_file(code, output_files)