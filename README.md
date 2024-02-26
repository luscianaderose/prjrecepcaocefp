# APLICAÇÃO DA RECEPÇÃO DE CÂMARAS 
## CONGREGAÇÃO ESPÍRITA FRANCISCO DE PAULA

## Comandos para o terminal em linux:

Para se conectar à VM da AWS:
```
ssh -i "chave_vm_cefp.pem" ubuntu@ec2-15-228-49-245.sa-east-1.compute.amazonaws.com
```

Para  se conectar à VM da AWS encurtando um passo: 
```
ssh ubuntu@ec2-15-228-49-245.sa-east-1.compute.amazonaws.com
```
Deu certo:
```
ssh -i "~/.ssh/chave_vm_cefp.pem" ubuntu@ec2-15-228-49-245.sa-east-1.compute.amazonaws.com
```

Para fazer o build da imagem Docker:
```
sudo docker build -t prjrecepcaocefp .
```