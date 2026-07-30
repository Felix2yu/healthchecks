# Arduino

从 Arduino 项目发送 ping 最简单的方式是使用
[ArduinoHttpClient](https://github.com/arduino-libraries/ArduinoHttpClient) 库。

以下代码使用 [WiFiNINA](https://www.arduino.cc/reference/en/libraries/wifinina/)
网络库，并在 Arduino Nano 33 IoT 板上测试通过。
ArduinoHttpClient 也适用于许多其他网络库，
包括 [Ethernet](https://github.com/arduino-libraries/Ethernet) 和
[ESP8266WiFi](https://arduino-esp8266.readthedocs.io/en/latest/esp8266wifi/readme.html)。

```c
#include <ArduinoHttpClient.h>
#include <WiFiNINA.h>

WiFiSSLClient wifi;
HttpClient client = HttpClient(wifi, "hc-ping.com", 443);

void setup() {
  Serial.begin(9600);
  while (!Serial);

  Serial.print("正在连接...");
  WiFi.begin("your-network-ssid", "your-network-password");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.print("\n已连接，IP 地址：");
  Serial.println(WiFi.localIP());

  // 发起 HTTPS 请求：
  client.get("/your-uuid-here");
  Serial.print("状态码：");
  Serial.println(client.responseStatusCode());
  Serial.print("响应：");
  Serial.println(client.responseBody());
}

void loop() {
}
```

注意：为简便起见，此示例中网络 SSID、密码和
检查项的代码是硬编码的。在实际代码中，建议
[将它们存储在 SECRET_ 字段中](https://docs.arduino.cc/arduino-cloud/tutorials/store-your-sensitive-data-safely-when-sharing)。
