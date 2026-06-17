"""
Para desarrollar el problema del inventario.

"""
from math import exp, factorial 
from MDPs import MDP, iteracion_valor

class Inventario(MDP):
    """
    Clase que representa un MDP para la empresa necroelectronica
    s = {-20, ..., 20}
    a = {0, ..., 20 - s}
    
    
    """    
    
    def __init__(self, gama,lambda_): 
        self.gama    = gama
        self.lambda_ = lambda_
        self.estados = tuple(range(-20, 21))

    def acciones_legales(self, s):
        return range(0, 20 - s +1)
    
    def recompensa(self, s, a, s_):
        return -(80 * a + (40 if a > 0 else 0)) + sum(
            (exp(-self.lambda_) * self.lambda_**d / factorial(d)) * (
                150 * max(0, min(d, s + a)) -
                  5 * max(0, (s + a) - d) -
                 85 * max(0, d - (s + a))
            )
            for d in range(20)
        )

        
    def prob_transicion(self, s, a, s_):
        if s_ > s + a or s_ < -20:
            return 0.0
        if s_ == -20:
            return 1 - sum(exp(-self.lambda_) * self.lambda_**d / factorial(d) for d in range(s + a + 20))
        return exp(-self.lambda_) * self.lambda_**(s + a - s_) / factorial(s + a - s_)

                
    def es_terminal(self, s):
        return False


if __name__ == "__main__":

    inventario = Inventario(0.9, 4)  

    pi_star, V = iteracion_valor(inventario, 1e-4, 2_000, True) 
    
    print("-" * 60)
    print("Estado".center(20) + "Acción".center(20) + "Valor".center(20))
    print("-" * 60 )
    for s in pi_star:
        print(f"{s:^20}{pi_star[s]:^20}{V[s]:^20.2f}")
    print("-" * 60)


"""
Contesta las preguntas aquí mismo (has espacio entre las preguntas):

1. ¿Cómo se comporta las transiciones y las ganancias para casos específicos de $s$ y $a$? 
2. ¿Qué psa si hay mucho almacen? 
3. ¿Que pasa si hay muy poco o estamos sin almacen? 
4. ¿Existe un punto donde la ganancia sea máxima?  
---
5. ¿Cómo se ve la política óptima? ¿Tiene sentido?
6. ¿Como se comporta la función de valor de estado V(s)?
7. ¿Cómo cambiaría la política si la variabilidad de la demanda (lambda) aumenta de 4 a 8?

"""