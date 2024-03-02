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


cd "F:\_dev aula lucas joy\prjrecepcaocefp"

Para fazer zip:
Compress-Archive "F:\_dev aula lucas joy\prjrecepcaocefp" "F:\_dev aula lucas joy\prjrecepcaocefp.zip" 

Enviar para a VM:
scp -i "~/.ssh/chave_vm_cefp.pem" "F:\_dev aula lucas joy\prjrecepcaocefp.zip" ubuntu@ec2-15-228-49-245.sa-east-1.compute.amazonaws.com:~

~. para encerrar

rm -rf prjrecepcaocefp
unzip prjrecepcaocefp.zip
ls pra listar

Para fazer o build da imagem Docker:
```
sudo docker build -t prjrecepcaocefp .
```
sudo docker ps

parar container:
 sudo docker stop aa7c989e6040
 sudo docker run -it -p 80:5000 prjrecepcaocefp

 .\deploy.ps1