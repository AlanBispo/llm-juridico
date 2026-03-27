import asyncio
from decimal import Decimal

from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.models.processo_model import ProcessoModel, TipoProcesso


PROCESSOS_MOCK = [
    {
        "numero": "0000001-99.2026.8.26.0001",
        "tipo": TipoProcesso.CIVEL,
        "resumo_peticao": (
            "Consumidora relata cobranca recorrente por servico de assinatura ja cancelado, "
            "com negativa de estorno administrativo e manutencao indevida em cadastro interno."
        ),
        "valor_pedido": Decimal("12500.00"),
        "historico_cliente": (
            "Cliente pessoa fisica, sem litigios anteriores no escritorio, busca solucao rapida "
            "e acordo se houver devolucao integral e danos morais proporcionais."
        ),
    },
    {
        "numero": "0000002-15.2026.5.02.0010",
        "tipo": TipoProcesso.TRABALHISTA,
        "resumo_peticao": (
            "Empregado alega jornada habitual superior a dez horas diarias, ausencia de "
            "pagamento correto de horas extras e supressao parcial do intervalo intrajornada."
        ),
        "valor_pedido": Decimal("48750.90"),
        "historico_cliente": (
            "Cliente ex-funcionario de empresa de logistica, possui documentos, conversas e "
            "espelhos de ponto incompletos para reforcar a narrativa inicial."
        ),
    },
    {
        "numero": "0000003-22.2026.8.19.0007",
        "tipo": TipoProcesso.PENAL,
        "resumo_peticao": (
            "Investigado responde por receptacao culposa em razao da compra de equipamento "
            "eletronico sem nota fiscal, afirmando desconhecer a origem ilicita do bem."
        ),
        "valor_pedido": Decimal("5000.00"),
        "historico_cliente": (
            "Cliente primario, com bons antecedentes, colaborou na entrega voluntaria do bem "
            "e busca estrategia voltada para resposta defensiva inicial."
        ),
    },
    {
        "numero": "0000004-08.2026.4.03.6100",
        "tipo": TipoProcesso.TRIBUTARIO,
        "resumo_peticao": (
            "Empresa questiona autuacao fiscal por suposto creditamento indevido de PIS e "
            "COFINS, alegando erro de enquadramento das despesas consideradas essenciais."
        ),
        "valor_pedido": Decimal("132400.35"),
        "historico_cliente": (
            "Cliente empresarial do setor industrial, com contabilidade organizada e interesse "
            "em medida judicial para suspender exigibilidade e discutir o merito."
        ),
    },
    {
        "numero": "0000005-44.2026.8.26.0100",
        "tipo": TipoProcesso.CIVEL,
        "resumo_peticao": (
            "Locatario pleiteia revisao de clausulas contratuais e devolucao de valores "
            "cobrados a titulo de reparos que corresponderiam a desgaste natural do imovel."
        ),
        "valor_pedido": Decimal("18990.00"),
        "historico_cliente": (
            "Cliente antigo do escritorio, perfil conciliador, ja tentou composicao extrajudicial "
            "sem sucesso e reuniu laudo fotografico da entrega das chaves."
        ),
    },
]


async def seed_processos() -> None:
    async with AsyncSessionLocal() as session:
        numeros = [processo["numero"] for processo in PROCESSOS_MOCK]
        resultado = await session.execute(
            select(ProcessoModel.numero).where(ProcessoModel.numero.in_(numeros))
        )
        existentes = set(resultado.scalars().all())

        novos_processos = []
        for processo in PROCESSOS_MOCK:
            if processo["numero"] in existentes:
                continue
            novos_processos.append(ProcessoModel(**processo))

        if not novos_processos:
            print("Nenhum novo processo para inserir. Seed ja estava aplicada.")
            return

        session.add_all(novos_processos)
        await session.commit()

        print(f"{len(novos_processos)} processos ficticios inseridos com sucesso.")


if __name__ == "__main__":
    asyncio.run(seed_processos())
