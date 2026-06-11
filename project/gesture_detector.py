class GestureDetector:
    def __init__(self):
        # IDs dos Landmarks: 4(Polegar), 8(Indicador), 12(Médio), 16(Anelar), 20(Mínimo)
        self.tip_ids = [4, 8, 12, 16, 20]

    def get_gesture(self, lm_list):
        """
        Analisa os landmarks e retorna o nome do gesto detectado ou None.
        Lógica:
        - Joinha: [1, 0, 0, 0, 0] (Apenas Polegar aberto)
        - Hang Loose: [1, 0, 0, 0, 1] (Polegar e Mínimo abertos)
        """
        if not lm_list:
            return None

        fingers_open = []

        # 1. Analisar Polegar (Verticalidade)
        if lm_list[4][2] < lm_list[2][2]:
            fingers_open.append(1)
        else:
            fingers_open.append(0)

        # 2. Analisar os outros 4 dedos
        for i in range(1, 5):
            tip_id = self.tip_ids[i]
            pip_id = tip_id - 2
            if lm_list[tip_id][2] < lm_list[pip_id][2]:
                fingers_open.append(1)
            else:
                fingers_open.append(0)

        # Classificação do Gesto
        if fingers_open == [1, 0, 0, 0, 0]:
            return "joinha"
        elif fingers_open == [1, 0, 0, 0, 1]:
            return "hang_loose"
        
        return None
