import requests
import random

# Criar um novo baralho
url = "https://deckofcardsapi.com/api/deck/new/shuffle/?cards=2H,3H,4H,5H,6H,7H,2D,3D,4D,5D,6D,7D,2S,3S,4S,5S,6S,7S,2C,3C,4C,5C,6C,7C"
response = requests.get(url)

if response.status_code == 200:
    try:
        data = response.json()
        deck_id = data["deck_id"]
        print(f"Baralho criado. Id do baralho {deck_id}")
    except ValueError:
        print("Erro: A resposta da API não contém JSON válido")
else:
    print(f"Erro ao acessar a API. Código de status: {response.status_code}")
    print("Conteúdo da resposta:", response.text)

# Função para virar uma carta na mesa
def virar_carta(deck_id):
    draw_url = f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=1'
    response = requests.get(draw_url)
    if response.status_code == 200:
        data = response.json()
        if 'cards' in data:
            carta_virada = data['cards'][0]
            print(f"Carta virada na mesa: {carta_virada['value']} de {carta_virada['suit']}")
            return carta_virada
        else:
            print("Erro: A chave 'cards' não foi encontrada na resposta.")
            return None
    else:
        print("Erro ao virar a carta. Verifique a conexão com a API.")
        return None

# Função para distribuir as cartas
def distribuir_cartas(deck_id, count=3):
    draw_url = f'https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count={count}'
    response = requests.get(draw_url)
    if response.status_code == 200:
        data = response.json()
        if 'cards' in data:
            return data["cards"]
        else:
            print("Erro: A chave 'cards' não foi encontrada na resposta.")
            return []
    else:
        print("Erro ao distribuir as cartas. Verifique a conexão com a API.")
        return []

# Sequência de força das cartas (como mencionado)
forca_cartas = {
    '3': 10, '2': 9, 'A': 8, 'K': 7, 'J': 6, 'Q': 5, '7': 4, '6': 3, '5': 2, '4': 1
}

# Função para verificar se a carta é manilha (superior à carta virada)
def eh_manilha(carta, carta_virada):
    valor_carta_virada = carta_virada['value']
    if forca_cartas[carta['value']] == forca_cartas[valor_carta_virada] + 1:
        return True
    return False

# Função para comparar as cartas com base na força
def comparar_cartas(carta1, carta2, carta_virada):
    if eh_manilha(carta1, carta_virada) and not eh_manilha(carta2, carta_virada):
        return 1  # Jogador 1 ganha
    elif eh_manilha(carta2, carta_virada) and not eh_manilha(carta1, carta_virada):
        return -1  # Jogador 2 ganha
    else:
        if forca_cartas[carta1['value']] > forca_cartas[carta2['value']]:
            return 1
        elif forca_cartas[carta1['value']] < forca_cartas[carta2['value']]:
            return -1
        else:
            return 0

# Função para jogar uma rodada
def jogar_rodada(cartas_jogador1, cartas_jogador2, carta_virada):
    print("\nJogando uma rodada...")
    
    # Comparar as cartas de ambos os jogadores
    vencedor_rodada = comparar_cartas(cartas_jogador1[0], cartas_jogador2[0], carta_virada)
    
    if vencedor_rodada == 1:
        return "Jogador 1"
    elif vencedor_rodada == -1:
        return "Jogador 2"
    else:
        return "Empate"

# Virar a carta na mesa (definir manilha)
carta_virada = virar_carta(deck_id)

if carta_virada:
    # Distribuir as cartas para os jogadores
    cartas_jogador1 = distribuir_cartas(deck_id)
    cartas_jogador2 = distribuir_cartas(deck_id)

    # Exibir as cartas
    print('\nCartas do Jogador 1')
    for carta in cartas_jogador1:
        print(f"{carta['value']} de {carta['suit']}")

    print('\nCartas do Jogador 2')
    for carta in cartas_jogador2:
        print(f"{carta['value']} de {carta['suit']}")

    # Jogar uma rodada
    rodada = jogar_rodada(cartas_jogador1, cartas_jogador2, carta_virada)
    print(f"\nResultado da rodada: {rodada}")
else:
    print("Não foi possível virar a carta, o jogo não pode continuar.")
