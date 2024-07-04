import { useState } from "react"
import axios from "axios"

function FormAtendido (props) {
    const [nomeAtendido, setNomeAtendido] = useState(props.pessoaNome)
    const editarAtendido = async (evento) => {
        evento.preventDefault()
        const resposta = await axios.get(`http://127.0.0.1:5001/editar_atendido_confirmado?nome_fila=${props.nomeFila}&numero_atendido=${props.numeroAtendido}&nome_atendido=${nomeAtendido}`)
        window.location.reload()
    }

    const linha = (
        <><br></br>____________________________________________________________<br></br><br></br></>
    )
    const desriscar = (
        <>
        {linha}
        <p>Deseja desriscar o nome?</p>
        <a href="/desriscar?numero_atendido={numero_atendido}&nome_fila={nome_fila}">
            <button>DESRISCAR</button>
        </a>
        {linha}
        Cancelar
        </>
    )

    return (
        <>
            <p>Deseja editar o nome?</p>
            <form onSubmit={(evento) => editarAtendido(evento)}>
                <input 
                    type='text' 
                    name='nome_atendido' 
                    value={nomeAtendido} 
                    onChange={(evento) => setNomeAtendido(evento.target.value)}
                />
                <input type='hidden' name='nome_fila' value={props.nomeFila}/>
                <input type='hidden' name='numero_atendido' value={props.numeroAtendido}/>
                <button type='submit' className='btj'>CONFIRMAR</button>
            </form>
            {desriscar ? props.pessoaEstado === "riscado" : ""}
        </>
    )
}

export default FormAtendido