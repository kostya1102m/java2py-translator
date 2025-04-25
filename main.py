import os
from adapters.translator import translate

if __name__ == "__main__":

    base_dir = os.path.dirname(__file__)  
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
   
    input_file = os.path.join(input_dir, "Example.java")
    output_file = os.path.join(output_dir, "Example.py")
    
  
    if not os.path.exists(input_file):
        java_code = """
        class Example {
            public static void main() {
                int x = 5 + 3 * 2;
                if (x == 10) {
                    int y = 20;
                }
                while (x == 10) {
                    int z = 30;
                }
            }
        }
        """
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write(java_code)
    
   
    try:
        generated_file = translate(input_file, output_file)
        print(f"Translation successful! Output written to: {generated_file}")
        
    except Exception as e:
        print(f"Error during translation: {e}")