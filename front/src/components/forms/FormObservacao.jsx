import axios from "axios"
import { useState } from "react"

function FormObservacao(props) {
    const [observacao, setObservacao] = useState(props.observacao)
    const adicionarObservacao = async(evento) => {
        evento.preventDefault()
        const resposta = await axios.get(`http://127.0.0.1:5001/observacao?nome_fila=${props.nomeFila}&numero_atendido=${props.numeroAtendido}&observacao=${observacao}`)
        window.location.reload()
    }

    return(
        <form onSubmit={(evento) => adicionarObservacao(evento)}>
            <input 
                type="text" 
                name="observacao" 
                value={observacao} 
                placeholder="Digite a observação"
                onChange={(evento) => setObservacao(evento.target.value)}
            />
            <button type="submit">OK</button>
        </form>
    )
}

export default FormObservacao