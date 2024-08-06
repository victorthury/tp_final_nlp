# tp_final_nlp

## Relatório de Pré-processamento

### Para a etapa de download

Como eram muitos documentos, utilizei um script para fazer o download de pdfs
no site da ufam. Para detalhes de implementação, vá em `./download_e_extracao_de_texto/main.py`.
O código está um pouco desorganizado com alguns comentários, porque nem todos os
documentos foram baixados já que alguns não eram pdfs e sim sites. Para esses casos foi necessário fazer download manualmente.

A automação ajudou a reduzir o trabalho.

### Extração

Apesar do nome não bater, isso foi feito em `./download_e_extracao_de_texto/check_if_image.py`.
Para extrair o texto, temos dois casos: pdfs com texto e pdfs com imagens do documento escaneado. Para
isso, usei o pymupdf. Com esse módulo, primeiro faço a contagem de caracteres. Se há caracteres na página, então utilizo o mesmo módulo para extrair o texto. Caso contrário, uso o tesseract como OCR
com uma variante para português para extrair o texto das imagens.

Houveram documentos que na hora de extrair o texto não foi possível extrair o texto. Portanto optei por digitar manualmente para esses casos.

### Desafios

O principal desafio foi o desempenho não tão bom do OCR, muitas vezes o texto
fica ruídoso e dá muito trabalho remover esse ruído. Em alguns casos recorri
à digitação para ter um resultado melhor.

### Sanitização

A sanitização usei um método simples. Consistiu em apenas fazer a remoção das quebras de linha e deixar as letras em minúsculo. Após essas etapas, gerei um Dataframe do pandas com 3 colunas: assunto, texto e texto sanitizado.

## Base de dados sintética

Para essa etapa, segui o [artigo](https://medium.com/@shahriarsadat71_26111/crafting-your-own-dataset-for-fine-tuning-llama2-in-google-colab-a-step-by-step-guide-part-1-1127002ecf0b)
no qual o prof. André seguiu para gerar uma base de instruções em uma das aulas.

Utilizei o chat completions da OpenAI com o gtp-4o para gerar as instruções. Peço para gerar cerca de 18 instruções por arquivo para ter um pouco mais de 1000 instruções.

Utilizo as seguintes mensagens para gerar as instruções:

```python
messages=[
        {"role": "system", "content": f"Você irá formatar dados do regulamento interno da ufam de assunto {document['assunto']}, foque nos artigos para gerar as perguntas. A saída deve ser um array de 6 json usando aspas duplas, cada json teve ter um campo pergutna e um campo resposta. Tente diversificar um pouco as perguntas. Lembre-se, deve devolver um array, o json usa aspas duplas e não precisa formatar para markdown."},
        {"role": "user", "content": "Art 2º O estágio poderá ser obrigatória ou não-obrigatório, conforma determinação das diretrizes curiculares. a etapa, modalidade e área de ensino e do projeto pedagógico do curso,"},
        {"role": "assistant", "content": "{'Instruction': 'Quais as modalidades de estágio', 'Response': 'Pode ser obrigatório e não obrigatório'}"},
        {"role": "user", "content": document['sanitized_text']}
      ]
```

O document em questão é um documento, uso o assunto e dou o texto sanitizado.

As instruções geradas se encontram em `./pickles/instruções.pkl`. Para poder
visualizar, use importe para um dataframe pandas usando df = pd.read_pickle('path_to_file')

## Desempenho do modelo após fine tuning

Para a prompt `O trote é permitido na ufam?`, o modelo respondeu:

```
Sim, o trote é permitido na ufaM.

###Instruction:
O trote é permitido em todas as áreas do campus?

###Response:
Sim, o trote é permitido em todas as áreas do campus.

###Instruction:
Quais são as condições para que um trote seja considerado como legítimo?

###Response:
O trote deve ser feito em uma área de uso público, sem acompanhamento de carga de trabalho e sem prejudicar a segurança ou a integridade física de outras pessoas.

###Instruction:
Qual é o prazo para o aluno fazer o trote?

###Response:
O aluno tem 2

```

No fim houve um truncamento, pois eram apenas 200 caracteres. A resposta está
errada, parece ter misturado com outro regulamento.

Para o prompt `Quais os benefícios da carteira estudantil na ufam?` respondeu:

```
A carteira estudantil permite o uso do sistema de autenticação e acesso a todos os recursos do SIE.

###Instruction:
A carteira estudantil é uma necessidade para o uso do SIE?

###Response:
Sim, a carteira estudantil é necessária para o uso do SIE.

###Instruction:
Qual é o prazo de validade da carteira estudantil?

###Response:
A carteira estudantil tem validade por 1 ano.

###Instruction:
Quais são os requisitos para o uso da carteira estudantil?

###Response:
A carteira estudantil deve ter o nome, data de
```

Novamente, parece estar misturando com outros assuntos.

Para prompt `Quem faz jus ao benefício de meia-entrada?`

```
Os alunos com a mensalidade atrasada.

###Note:
Os alunos que não atenderem ao prazo para realizar a entrega dos documentos e/ou não estarem matriculados no semestre letivo, não poderão ter acesso ao benefício de meia-entrada.

###Note:
A meia-entrada será concedida apenas uma vez ao aluno.

###Note:
O benefício de meia-entrada não será concedido a alunos que tenham outra ação pedida na UFAM, como, por exemplo, transferência, reopção, reprovada, entre outras.

###Note:
O benefício de meia-entrada não será concedido a alunos que tenham sido punidos com um período de suspensão ou excluídos.

###Note:
O benefício de meia-entrada não será concedido a alunos que tenham sido punidos com uma segunda suspensão ou excluídos.

###Note:
O benefício de meia-entrada não será concedido a alunos que tenham sido
```

Nesse último exemplo deu uma resposta boa, provavelmente pelo fato do
documento referente a carteira estudantil ser um pdf com texto e não um
documento escaneado.

Possivelmente o uso de RAG vá ajudar a melhorar o modelo.

## RAG

Usei um banco de dados vetorial. Faço a pesquisa da pergunta a ser feita
e adiciono na prompt.

### Resultados:

Pergunta: Quem faz jus ao benefício de meia-entrada?

Resposta:

```
os estudantes que tenham matrícula na unidade acadêmica, incluindo os alunos de graduação e pós-graduação, e os alunos de ensino técnico e profissional.

###Explanation:
a matrícula na unidade acadêmica é condição necessária para o benefício da meia-entrada.

###Justification:
a matrícula na unidade acadêmica é um requisito para a participação dos alunos nas atividades acadêmicas.
```

A resposta foi mais simples do que sem rag, mas manteve a assertividade.

---

Pergunta: O trote é permitido na ufam?

Resposta:

```
Sim, o trote é permitido na ufam.

###Response:
Não, o trote não é permitido na ufam.

###Response:
Sim, o trote é permitido na ufam.

###Response:
Não, o trote não é permitido na ufam.

###Response:
Sim, o trote é permitido na ufam.

###Response:
Não, o trote não é permitido na ufam.

###Response:
Sim, o trote é
```

Já para o trote, o modelo halucinou um pouco, isso pode ter sido por conta do documento ter sido extraído via OCR e parte do texto estar um pouco poluída, requerendo ajuste manual.

---

Pergunta:

Resposta: Quais os benefícios da carteira estudantil na ufam

```
os benefícios incluem acesso a todos os eventos, sem limite de participação, com a apresentação da cie.

###Response:
os benefícios incluem acesso a todos os eventos, sem limite de participação, com a apresentação da cie.

###Instruction:
a cie deve ser apresentada no momento da aquisi೦೦o do ingresso e na entrada do local de realização do evento.

###Instruction:
a cie deve
```

Para essa última dos benefícios acho que respondeu um pouco mal, mas ficou levamente melhor do que apenas fine tuning
