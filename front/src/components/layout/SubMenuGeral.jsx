import axios from "axios"
import styles from "./Menu.module.css"
import audioSilencioMp3 from "../../assets/audio/celulares_silencio.mp3"


function SubMenuGeral (props) {

    const reinicarTudo = async () => {
        const resposta = await axios.get("http://127.0.0.1:5001/reiniciar_tudo_confirmado")
        window.location.reload()
    }

    const pedirSilencio = async () => {
        const audio = new Audio(audioSilencioMp3)
        audio.play()
    }

    return (
        <div className={`${styles.divMenu} cor-fundo2`}>
                <a href="/tv">
                    <button>TV</button>
                </a>

                <a href="/info">
                    <button>INFORMAÇÕES</button>
                </a>

                <a onClick={() => pedirSilencio()}>
                    <button>PEDIR SILÊNCIO</button>
                </a>

                <a onClick={() => reinicarTudo()}>
                    <button>REINICAR TUDO</button>
                </a>
        </div>
    
    )
}

export default SubMenuGeral