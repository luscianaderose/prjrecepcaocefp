#Para fazer zip:
Compress-Archive -Update "F:\_dev aula lucas joy\prjrecepcaocefp" "F:\_dev aula lucas joy\prjrecepcaocefp.zip" 

#Enviar para a VM:
scp -i "~/.ssh/chave_vm_cefp.pem" "F:\_dev aula lucas joy\prjrecepcaocefp.zip" ubuntu@ec2-15-228-49-245.sa-east-1.compute.amazonaws.com:~

ssh -i "~/.ssh/chave_vm_cefp.pem" ubuntu@ec2-15-228-49-245.sa-east-1.compute.amazonaws.com "sudo rm -rf prjrecepcaocefp &&\
echo descomprimindo arquivos do projeto &&\
unzip prjrecepcaocefp.zip ;\
echo ok descomprimindo arquivos do projeto &&\
cd prjrecepcaocefp &&\
sudo docker build -t prjrecepcaocefp . &&\
sudo docker ps &&\
sudo docker stop prjrecepcaocefp-app ;\
sudo docker run -d -p 80:5000 --name prjrecepcaocefp-app --rm prjrecepcaocefp"