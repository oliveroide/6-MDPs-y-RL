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
Como tenemos nuestra delta fijada en 4 las probabilidades de las transciciones tambien estan fijas, las ganancias por el otro lado varian dependiendo los valores de s y de a, el nivel optimo de productos en el inventario debe ser de 6-8 por lo que entre s este mas cerca de 6-8 y a sea 0-2 la recompensa va a ser mas alta, si s es baja y a es grande la recompensa sera menor porque tiene costo esas compras, si el inventario es muy negativo y a es pequeña la recompensa sera negativa y muy baja, si tanto s como a son muy grandes tambien la recompensa sera negativa por los costoso de ordenar y los de guardar inventario 

2. ¿Qué psa si hay mucho almacen? 
entre mas se aleja del nivel optimo menor se vuelve la recompensa por los costos de mantener el inventario y la accion optima seria no comprar mas inventario a = 0
3. ¿Que pasa si hay muy poco o estamos sin almacen? 
Si hay muy pocos, nada o negativo la recompensa sera negativa y extremandamente baja, la unica forma de arreglar eso es haciendo un pedido lo suficientemente grande para llegar al nivel optimo de mercancia 
4. ¿Existe un punto donde la ganancia sea máxima?  
Si, en que s + a = 9 porque el modelo prefiere tener unidades que le sobren a que tener la penalizacion de que le faten
5. ¿Cómo se ve la política óptima? ¿Tiene sentido?

6. ¿Como se comporta la función de valor de estado V(s)?
7. ¿Cómo cambiaría la política si la variabilidad de la demanda (lambda) aumenta de 4 a 8?

"""