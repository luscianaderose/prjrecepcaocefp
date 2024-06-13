import styles from "./Info.module.css"
import chamarComSomPng from "../../assets/img/chamar-com-som.png"
import chamarSemSomPng from "../../assets/img/chamar-sem-som.png"
import cancelarPng from "../../assets/img/cancelar.png"
import duplaPng from "../../assets/img/dupla.png"
import duplaCancelarPng from "../../assets/img/dupla_cancelar.png"



function Info(){
    return(
        <div className={`${styles.divInfo} cor-fundo2`}>
            <details>
                <summary className="txt-tit2">INFORMAÇÕES</summary>
                {/* <!-- texto_recepcao --> */}
                <p className="txt-tit3">ROTINA DA RECEPÇÃO DAS CÂMARAS</p>
                    <ol>
                        <li>Verificar no comprovante de agendamento da pessoa se data da marcação é a data de hoje.</li>
                        <li>Digitar o nome, escolher a fila correspondente (prece ou vidência) e clicar em 'ADICIONAR'.</li>
                        <li>Carimbar o comprovante.</li>
                        <li>Anotar o número da ordem de chegada no comprovante.</li>
                        <li>Devolver o comprovante para a pessoa.</li>
                        <li>Pedir para se sentar segurando o comprovante em mãos.</li>
                        <li>Quando a câmara chamar, clicar no botão 'CHAMAR PRÓXIMO' ou na bola com número da câmara.</li>
                        <li>Automaticamente o nome anterior é riscado na lista, a câmara que chamou fica registrada ao lado do nome na lista, uma bolinha vazia fica preenchida e um áudio é tocado avisando que a câmara está chamando.</li>
                        <li>Chamar o próximo pelo nome da pessoa. Mostrar à pessoa onde é a câmara.</li>
                        <li>Nas sextas-feiras, normalmente cada câmara atende 5 pessoas. Quando 5 bolinhas forem preenchidas, é hora de avisar a câmara que é a última.</li>
                        <li>Se comparecerem menos de 10 pessoas em uma lista, tente dividir igualmente entre as câmaras. Por exemplo, se comparecerem apenas 8 pessoas para cada câmara de uma lista, direcione 4 para cada câmara para distribuir o trabalho igualmente.</li>
                        <li>Ao entrar a última pessoa da câmara, avisar ao secretário da câmara que é a última pessoa a ser atendida para que a câmara possa fazer depois dela o processo de encerramento.</li>
                        <li>Leia um trecho do Evangelho às 18:50. Falar a saudação da casa antes e depois (Graças a Deus, a Jesus e a Francisco de Paula). Se quiser pode rezar o Pai Nosso. Fale os seguintes avisos: silêncio, desligar os celulares, comprovante em mãos, pode pegar um livro do balcão para ler enquanto espera.</li>
                    </ol>
                
                    <p className="txt-tit3">REPETIR CHAMADO COM OU SEM SOM</p>
                    <ul>
                        <li>Clique em <img alt="chamar com som" src={chamarComSomPng} width="12" height="12"/> para repetir o chamado com som.</li>
                        <li>Clique em <img alt="chamar sem som" src={chamarSemSomPng} width="12" height="12"/> para repetir o chamado sem som, fazendo apenas o destaque visual.</li>
                    </ul>
                    
                    <p className="txt-tit3">NOMES QUE ENTRAM JUNTOS NA CÂMARA – CRIAÇÃO DE DUPLA</p>
                    <ol>
                        <li>Na lista de nomes da fila, clique no botão CRIAR DUPLA <img alt="dupla" src={duplaPng} width="16" height="16"/> ao lado do nome que formará dupla.</li>
                        <li>Este ícone se tornará um <img alt="x" src={cancelarPng} width="16" height="16"/>. Caso queira cancelar a ação, clique neste <img alt="cancelar" src={cancelarPng} width="16" height="16"/>.</li>
                        <li>Agora clique no botão CRIAÇÃO DE DUPLA <img alt="dupla" src={duplaPng} width="16" height="16"/> ao lado do nome que entrará na câmara junto. Pronto!</li>
                        <li>Se quiser desfazer, clique no botão DESFAZER DUPLA <img alt="cancelar dupla" src={duplaCancelarPng} width="16" height="16"/>.</li>
                    </ol>
                    <br></br><br></br>
            </details>
            {/* <!-- get_calendario() --> */}
            <div className={`${styles.diCalendario} cor-fundo3`}>
                <pre>
                                                    2024

janeiro                                              fevereiro                                               março
seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom
1      2      3      4      5      6      7                                1      2      3      4                                       1      2      3
8      9     10     11     12     13     14           5      6      7      8      9     10     11           4      5      6      7      8      9     10
15     16     17     18     19     20     21          12     13     14     15     16     17     18          11     12     13     14     15     16     17
22     23     24     25     26     27     28          19     20     21     22     23     24     25          18     19     20     21     22     23     24
29     30     31                                      26     27     28     29                               25     26     27     28     29     30     31

 abril                                                  maio                                                 junho
seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom
1      2      3      4      5      6      7                         1      2      3      4      5                                              1      2
8      9     10     11     12     13     14           6      7      8      9     10     11     12           3      4      5      6      7      8      9
15     16     17     18     19     20     21          13     14     15     16     17     18     19          10     11     12     13     14     15     16
22     23     24     25     26     27     28          20     21     22     23     24     25     26          17     18     19     20     21     22     23
29     30                                             27     28     29     30     31                        24     25     26     27     28     29     30

 julho                                                 agosto                                               setembro
seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom
1      2      3      4      5      6      7                                1      2      3      4                                                     1
8      9     10     11     12     13     14           5      6      7      8      9     10     11           2      3      4      5      6      7      8
15     16     17     18     19     20     21          12     13     14     15     16     17     18           9     10     11     12     13     14     15
22     23     24     25     26     27     28          19     20     21     22     23     24     25          16     17     18     19     20     21     22
29     30     31                                      26     27     28     29     30     31                 23     24     25     26     27     28     29
                                                                                          30

outubro                                               novembro                                              dezembro
seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom         seg    ter    qua    qui    sex    sáb    dom
1      2      3      4      5      6                                       1      2      3                                                     1
7      8      9     10     11     12     13           4      5      6      7      8      9     10           2      3      4      5      6      7      8
14     15     16     17     18     19     20          11     12     13     14     15     16     17           9     10     11     12     13     14     15
21     22     23     24     25     26     27          18     19     20     21     22     23     24          16     17     18     19     20     21     22
28     29     30     31                               25     26     27     28     29     30                 23     24     25     26     27     28     29

                </pre>
            </div>
        </div>

    )
}

export default Info