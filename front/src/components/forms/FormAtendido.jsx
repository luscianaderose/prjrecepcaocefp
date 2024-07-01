function FormAtendido (props) {
    
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
            <form action='/editar_atendido_confirmado'>
                <input type='text' name='nome_atendido' value={props.pessoaNome}/>
                <input type='hidden' name='nome_fila' value={props.filaNome}/>
                <input type='hidden' name='numero_atendido' value={props.numeroAtendido}/>
                <button type='submit' class='btj'>CONFIRMAR</button>
            </form>
            {desriscar ? props.pessoaEstado === "riscado" : ""}
        </>
    )
}

export default FormAtendido