import subprocess
import os
#input_path = '../WIN_20230928_08_56_37_Pro.jpg'
#output_path = '../perspective_out.jpg'
def realesrgan(input_path):
    """Apply RealESRGAN to an image."""
    file_name, file_extension = os.path.splitext(input_path)
    output_path = file_name+'_out'+file_extension
    command = f'realesrgan-ncnn-vulkan.exe -i {input_path} -o {output_path}'

    try:
    # Run the command and capture the output and errors
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Check if the command was successful
        if result.returncode == 0:
            print("Command executed successfully.")
        # Print the standard output of the command
            print(result.stdout)
        else:
            print("Command execution failed.")
        # Print the standard error output of the command
            print(result.stderr)
    except Exception as e:
        print("An error occurred:", str(e))
    
    return output_path
        
#realesrgan(input_path, output_path)