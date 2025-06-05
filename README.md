# Detector de Luminosidade com ESP8266 e Raspberry Pi

Este projeto tem como objetivo desenvolver um sistema IoT simples e funcional para **monitoramento de luminosidade** com resposta visual automática (LED) e visualização de dados em tempo real por meio de um **dashboard gráfico implementado em Python**, rodando localmente na Raspberry Pi.

---

## Componentes Utilizados

- ESP8266 NodeMCU  
- Sensor de luminosidade LDR  
- LED + resistor de 220 ohms  
- Protoboard e jumpers  
- Raspberry Pi 3 B+  
- Conexão Wi-Fi  
- Broker MQTT (Mosquitto)  
- Dashboard em Python (Tkinter, Pandas, Seaborn, Matplotlib)

---

## Objetivo

Criar um sistema que:

1. **Meça a luminosidade do ambiente**  
2. **Envie os dados para um broker MQTT**  
3. **Acione um LED automaticamente quando estiver escuro**  
4. **Exiba os dados de forma gráfica e em tempo real em uma interface desenvolvida em Python**

---

## Tópicos MQTT

| Tópico                | Descrição                                | Exemplo de Payload |
|-----------------------|-------------------------------------------|--------------------|
| `sensor/light`        | Valor bruto do sensor LDR (0–1023)        | `724`              |
| `sensor/light_percent`| Luminosidade em porcentagem (0–100%)      | `71`               |
| `sensor/led_state`    | Estado do LED                             | `ON` ou `OFF`      |

---

## Esquema de Montagem

- O **LDR** está ligado ao pino **A0** da ESP8266 e ao **GND**, com resistor pull-up.  
- O **LED** está conectado ao pino **D1**, com resistor de 220 ohms em série.  
- A alimentação do circuito vem da própria ESP8266 (3.3V e GND).

---

## Trechos do Código Explicado

### Conexão com a rede Wi-Fi:

```cpp
WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
  delay(500);
  Serial.print(".");
}
```

Esse trecho conecta o ESP8266 à rede Wi-Fi. O programa espera até a conexão ser estabelecida.

---

### Leitura e envio dos dados:

```cpp
int ldrValue = analogRead(ldrPin);
String lightPercent = String(map(ldrValue, 0, 1024, 0, 100));
client.publish("sensor/light", String(ldrValue).c_str());
client.publish("sensor/light_percent", lightPercent.c_str());
```

Aqui, o valor do sensor é lido, convertido em porcentagem e enviado para o broker MQTT.

---

### Acionamento automático do LED:

```cpp
if (ldrValue < threshold) {
  digitalWrite(ledPin, HIGH);
  client.publish("sensor/led_state", "ON");
} else {
  digitalWrite(ledPin, LOW);
  client.publish("sensor/led_state", "OFF");
}
```

O LED é ligado ou desligado dependendo da intensidade de luz medida.

---

## Dashboard em Python

O painel de visualização foi construído com Python e exibe:

- O valor mais recente de luminosidade
- Um gráfico de linha com as **últimas 20 leituras**
- Interface simples e responsiva criada com `tkinter`

A cada nova leitura recebida via MQTT, o script:

1. Armazena o valor em um `DataFrame` com `timestamp`  
2. Atualiza o gráfico com `seaborn`  
3. Exibe o novo valor na janela

---

## Automação da execução

Para facilitar o uso, foi criado o script `run_project.sh`:

```bash
#!/bin/bash
cd ~/Documents/bolinho
source ~/Documents/bolinho/bolovenv
~/Documents/bolinho/bolovenv/bin/python3 ~/Documents/bolinho/client.py
```

Esse script ativa o ambiente virtual Python e executa o painel com um único comando.

---

## Problemas Enfrentados

- Mal contato entre o sensor LDR e a protoboard causou falhas de leitura.  
- Foram reforçadas as conexões físicas para garantir estabilidade.  

---

## Requisitos de Software

- Arduino IDE com suporte ao ESP8266  
- Biblioteca `PubSubClient` (ESP)  
- Broker MQTT (Mosquitto) na Raspberry Pi  
- Bibliotecas Python: `paho-mqtt`, `pandas`, `matplotlib`, `seaborn`, `tkinter`

---

## Como Rodar o Projeto

1. Suba o código da ESP8266 via Arduino IDE.  
2. Inicie o broker MQTT na Raspberry Pi.  
3. Execute o script `run_project.sh` para iniciar o dashboard.  
4. Verifique o monitor serial da ESP para acompanhar as conexões.  
5. Acompanhe a variação da luminosidade no painel gráfico.  

---

## Estrutura do Projeto

```
├── esp8266-firmware/
│   └── Código-fonte da ESP8266
├── raspberry-pi/
│   ├── client.py
│   ├── run_project.sh
│   └── bolovenv/ (ambiente virtual)
├── docs/
│   └── Projeto_IoT_Grupo1.pdf
└── README.md
```

---

## 👨‍🔬 Autores

- André Carvalho  
- Arthur Lins  
- Pedro Oliveira  
