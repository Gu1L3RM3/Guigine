# Engine Example Recipes

Esta pasta organiza exemplos basicos de uso da `Guigine`.

## Exemplos atuais

- `basic_scene.py`: jogo simples sem mapa
- `tmx_scene.py`: jogo com mapa TMX e spawns genericos
- `widgets_only_scene.py`: interface usando apenas widgets

## Assets locais

Os exemplos possuem um espelho proprio em:

- `examples/assets/`

Isso permite que a vitrine de exemplos rode de forma autocontida, sem depender de assets duplicados fora de `examples/` nem ficar misturada ao pacote `engine`.

## Runtime dos exemplos

Para subir os exemplos usando os assets locais, use:

```bash
python -m examples.run_examples
```
