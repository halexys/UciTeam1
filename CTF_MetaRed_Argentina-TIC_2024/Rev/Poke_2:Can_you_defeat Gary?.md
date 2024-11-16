# Rev / Poke 2: Can you defeat Gary?

Nos encontramos en medio de una batalla pokemon, debemos escoger rapido una opcion o el juego termina:

```
You're in a Pokémon battle against Gary to determine the league champion!
Gary has Sandslash (HP: 95), you have Pikachu (HP: 10).

You have 1 second for every choice.

What do you want to do?
1. Attack
2. Change Pokémon
3. Use item
4. Run

Too slow. Game over.
```

Podemos usar un desensamblador para ver que pasa, pero solo con ejecutar el programa podemos darnos cuenta de algunas cosas:

```
 ./pokemaster 
You're in a Pokémon battle against Gary to determine the league champion!
Gary has Sandslash (HP: 95), you have Pikachu (HP: 10).

You have 1 second for every choice.

What do you want to do?
1. Attack
2. Change Pokémon
3. Use item
4. Run
3

> 
Available items:
1. Potion - Restores 20 HP of a Pokémon's health
2. Antidote - Cures the poisoned state
3. Fresh water - Restores 50 HP of a Pokémon's health, don't confuse with the other
4. Max potion - Restores all HP
5. Branco's container - Eh: https://tinyurl.com/4hpeuztv
6. More PP - Adds more PP to a move
7. Back
5

> 
Which Pokémon do you want to use Branco's container on?
1. Charizard (fainted)
2. Venusaur (fainted)
3. Blastoise (fainted)
4. Butterfree (fainted)
5. Pidgeot (fainted)
6. Pikachu
8. Back

Too slow. Game over.
```

Si decidimos escoger un objeto, el numero 5 se ve sospechoso y cuando vamos a usar un objeto sobre un pokemon vemos que no hay opcion 7. Si seguimos este camino (3-5-7) veremos que funciona:

``` bash
 echo "flag{toy_flag}" > flag.txt # Creando una bandera de prueba en la maquina local
```

```
 You used Branco's container on Sandslash.
Sandslash's HP restored to 100...
Sandslash... feels sleepy... is confused... 
Sandslash fainted
Ash wins the battle!
You are the best Pokémon trainer ever, you deserve this: flag{toy_flag}
```

Probamos en el remoto y obtenemos la flag:

`flag{Alw4ys_lO0k_foR_Your_1nNer_Bilardo}`


