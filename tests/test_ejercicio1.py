# tests/test_ejercicio1.py
import json
import sys
import traceback
import re
from io import StringIO
import contextlib

class NotebookTester:
    def __init__(self, notebook_path):
        self.notebook_path = notebook_path
        self.score = 0
        self.max_score = 100
        self.results = []
        
    def load_notebook(self):
        """Carga el notebook y extrae el código Python"""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Extraer solo las celdas de código (no las de instalación)
            code_cells = []
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    source = ''.join(cell['source'])
                    # Ignorar celdas de instalación y imports de compatibilidad
                    if not (source.strip().startswith('pip install') or 
                           'collections.abc' in source):
                        code_cells.append(source)
            
            return '\n\n'.join(code_cells)
        except Exception as e:
            self.results.append(f"❌ Error cargando notebook: {e}")
            return None
    
    def test_imports_and_classes(self, code):
        """Verifica que las importaciones y clases estén definidas correctamente"""
        points = 0
        
        # Verificar import de experta
        if 'from experta import *' in code:
            points += 5
            self.results.append("✅ Import de experta correcto (5 pts)")
        else:
            self.results.append("❌ Falta import de experta")
        
        # Verificar definición de clases Fact
        required_classes = ['Symptom', 'CarState', 'Diagnosis', 'RepairAction', 'VehicleStatus']
        for class_name in required_classes:
            if f'class {class_name}(Fact):' in code:
                points += 2
                self.results.append(f"✅ Clase {class_name} definida correctamente (2 pts)")
            else:
                self.results.append(f"❌ Falta definición de clase {class_name}")
        
        # Verificar clase principal
        if 'class VehicleDiagnosis(KnowledgeEngine):' in code:
            points += 5
            self.results.append("✅ Clase VehicleDiagnosis definida correctamente (5 pts)")
        else:
            self.results.append("❌ Falta clase VehicleDiagnosis")
        
        return points
    
    def test_completed_rules(self, code):
        """Verifica que las reglas estén completadas correctamente"""
        points = 0
        
        # Test 1: Regla de frenos
        if re.search(r'@Rule\(Symptom\(tipo=[\'"]ruido_metalico[\'"]\),\s*salience=\d+\)', code):
            points += 15
            self.results.append("✅ Regla de frenos completada correctamente (15 pts)")
            
            if 'def frenos_problema(self):' in code or 'def problema_frenos(self):' in code:
                points += 5
                self.results.append("✅ Función de frenos nombrada correctamente (5 pts)")
        else:
            self.results.append("❌ Regla de frenos incompleta")
        
        # Test 2: Regla de refrigerante
        if re.search(r'@Rule\(AND\(.*Symptom\(tipo=[\'"]fuga_liquido[\'"].*CarState\(estado=[\'"]motor_caliente[\'"].*\),\s*salience=\d+\)', code):
            points += 15
            self.results.append("✅ Regla de refrigerante completada correctamente (15 pts)")
        else:
            self.results.append("❌ Regla de refrigerante incompleta")
        
        # Test 3: Regla NOT (revision general)
        if 'NOT(Symptom(tipo=' in code and 'def revision_general(self):' in code:
            points += 10
            self.results.append("✅ Regla de revisión general con NOT completada (10 pts)")
        else:
            self.results.append("❌ Regla de revisión general incompleta")
        
        return points
    
    def test_declare_statements(self, code):
        """Verifica que las declaraciones declare() estén completadas"""
        points = 0
        
        # Contar declares correctos
        declare_patterns = [
            r'self\.declare\(Diagnosis\(resultado=resultado\)\)',
            r'self\.declare\(RepairAction\(tipo=[\'"][^\'\"]+[\'"]\)\)',
            r'self\.declare\(VehicleStatus\(estado=[\'"][^\'\"]+[\'"]\)\)'
        ]
        
        for pattern in declare_patterns:
            if re.search(pattern, code):
                points += 5
                self.results.append("✅ Declaración declare() correcta (5 pts)")
        
        return points
    
    def test_retract_statements(self, code):
        """Verifica que las declaraciones retract() estén completadas"""
        points = 0
        
        if 'self.retract(fact)' in code:
            retract_count = code.count('self.retract(fact)')
            points += retract_count * 3
            self.results.append(f"✅ {retract_count} declaraciones retract() correctas ({retract_count * 3} pts)")
        else:
            self.results.append("❌ Faltan declaraciones retract()")
        
        return points
    
    def test_execution_section(self, code):
        """Verifica la sección de ejecución"""
        points = 0
        
        if 'engine = VehicleDiagnosis()' in code:
            points += 5
            self.results.append("✅ Instanciación del motor correcta (5 pts)")
        else:
            self.results.append("❌ Falta instanciación del motor")
        
        if 'engine.reset()' in code:
            points += 3
            self.results.append("✅ Reset del motor correcto (3 pts)")
        else:
            self.results.append("❌ Falta reset del motor")
        
        if 'engine.run()' in code:
            points += 5
            self.results.append("✅ Ejecución del motor correcta (5 pts)")
        else:
            self.results.append("❌ Falta ejecución del motor")
        
        # Verificar que hay declaraciones de síntomas
        if 'engine.declare(Symptom(' in code:
            symptom_count = code.count('engine.declare(Symptom(')
            if symptom_count >= 2:
                points += 7
                self.results.append(f"✅ {symptom_count} síntomas declarados correctamente (7 pts)")
            else:
                points += 3
                self.results.append(f"✅ {symptom_count} síntoma(s) declarado(s) (3 pts)")
        else:
            self.results.append("❌ Faltan declaraciones de síntomas")
        
        return points
    
    def test_syntax_and_execution(self, code):
        """Prueba si el código se ejecuta sin errores de sintaxis"""
        points = 0
        
        # Capturar output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            # Intentar compilar el código
            compile(code, '<string>', 'exec')
            points += 10
            self.results.append("✅ Sintaxis correcta - código compila (10 pts)")
            
            # Intentar ejecutar (con timeout implícito)
            exec_globals = {}
            exec(code, exec_globals)
            points += 5
            self.results.append("✅ Código ejecuta sin errores (5 pts)")
            
            # Verificar que hay output (el sistema debe imprimir diagnósticos)
            output = captured_output.getvalue()
            if output.strip():
                points += 5
                self.results.append("✅ El sistema genera output (5 pts)")
            
        except SyntaxError as e:
            self.results.append(f"❌ Error de sintaxis: {e}")
        except Exception as e:
            self.results.append(f"❌ Error de ejecución: {e}")
        finally:
            sys.stdout = old_stdout
        
        return points
    
    def run_tests(self):
        """Ejecuta todos los tests"""
        code = self.load_notebook()
        if not code:
            return
        
        # Ejecutar tests
        self.score += self.test_imports_and_classes(code)
        self.score += self.test_completed_rules(code)
        self.score += self.test_declare_statements(code)
        self.score += self.test_retract_statements(code)
        self.score += self.test_execution_section(code)
        self.score += self.test_syntax_and_execution(code)
        
        # Generar reporte
        self.generate_report()
    
    def generate_report(self):
        """Genera el reporte final"""
        percentage = (self.score / self.max_score) * 100
        
        report = f"""
{'='*60}
RESULTADOS DE AUTOCALIFICACIÓN - EJERCICIO 1 TALLER 1
{'='*60}

PUNTUACIÓN: {self.score}/{self.max_score} ({percentage:.1f}%)

DETALLES:
{chr(10).join(self.results)}

{'='*60}
CALIFICACIÓN FINAL: {percentage:.1f}%
{'='*60}
        """
        
        print(report)
        
        # Guardar resultados en archivo
        with open('test_results.txt', 'w', encoding='utf-8') as f:
            f.write(report)
        
        # Determinar si pasa o falla
        if percentage >= 70:
            print("🎉 ¡APROBADO! - El ejercicio cumple con los requisitos mínimos")
            sys.exit(0)
        else:
            print("❌ REPROBADO - El ejercicio necesita más trabajo")
            sys.exit(1)

if __name__ == "__main__":
    # Buscar el notebook
    import os
    notebook_files = [f for f in os.listdir('.') if f.endswith('.ipynb')]
    
    if not notebook_files:
        print("❌ No se encontró ningún archivo .ipynb")
        sys.exit(1)
    
    # Usar el primer notebook encontrado (o buscar específicamente el del ejercicio 1)
    target_notebook = None
    for nb in notebook_files:
        if 'ejercicio' in nb.lower() and '1' in nb:
            target_notebook = nb
            break
    
    if not target_notebook:
        target_notebook = notebook_files[0]
    
    print(f"Probando notebook: {target_notebook}")
    tester = NotebookTester(target_notebook)
    tester.run_tests()