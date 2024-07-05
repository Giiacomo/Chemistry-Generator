import subprocess

def run_script_until_2():
    command = ["python3", "main.py", "-generator", "-o", "test/output/output.txt", "test/input/00_chimica_test.txt", "-debug"]

    count_none = 0
    count_1 = 0
    count_3 = 0
    iterations = 0

    try:
        while True:
            # Esegui il comando
            result = subprocess.run(command, capture_output=True, text=True)
            output = result.stdout.strip()

            # Verifica l'output
            if "2" in output:
                print("Uscito il numero 2!")
                break
            elif "1" not in output and "3" not in output:
                count_none += 1
            elif "1" in output:
                count_1 += 1
            elif "3" in output:
                count_3 += 1

            iterations += 1
            print(f"Iterazione {iterations}: Numero diverso da 2, ripeto...")
            print(output)
    
    except KeyboardInterrupt:
        print("\nInterruzione manuale (Ctrl+C) ricevuta.")

    finally:
        print(f"Numero di volte in cui l'output era nulla: {count_none}")
        print(f"Numero di volte in cui l'output era 1: {count_1}")
        print(f"Numero di volte in cui l'output era 3: {count_3}")
        print(f"Numero totale di iterazioni: {iterations}")

if __name__ == "__main__":
    run_script_until_2()
