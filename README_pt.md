# heic-to-jpg

Uma jeito serverless de converter massivamente imagens do tipo HEIC para JPG quase instantaneamente usando S3 e Lambda.

Eu estava ajudando minha esposa, que queria imprimir algumas fotos da nossa família, mas a ferramenta que ela estava usando aceitava apenas imagens em JPG, e a maioria das fotos dela estava no formato HEIC.

Como bom nerd que sou, não fiquei satisfeito apenas em rodar um script local em Python para converter todas as fotos. Pensei: essa é uma ótima oportunidade para praticar a criação de uma aplicação serverless que faça isso. Usando o poder da computação em nuvem, imaginei que seria possível converter todas as imagens quase instantaneamente—e consegui!

Criei uma solução que usa S3 e Lambda para converter imagens em massa.

Aqui está como eu fiz isso...

# A Solução

![Arquitetura usando serviços AWS para converter em massa imagens HEIC para JPG](assets/architecture.png)

A ideia é simples. O S3 é um serviço de armazenamento de objetos onde posso armazenar qualquer tipo de arquivo com baixo custo. O S3 tem um recurso interessante chamado "Event Notifications". Com esse recurso, posso "escutar" diferentes eventos que ocorrem em um bucket (o local onde faço o upload dos arquivos).

Assim, para cada arquivo que eu envio, um evento é gerado, e ele é responsável por realizar a conversão para JPG. Para a conversão, utilizo uma função Lambda. O Lambda é um componente de Function-as-a-Service (FaaS) que permite executar código sem precisar se preocupar com infraestrutura. Ele é escalável e você só paga pelo uso.

Essa mesma função Lambda salva a imagem JPG em outro bucket S3, de onde posso baixá-la.

O mais interessante é que a conversão acontece quase instantaneamente. Isso porque tanto o S3 quanto o Lambda são serviços serverless, o que significa que eles respondem automaticamente com a escala necessária.

# Como usar

Para implantar essa solução, você precisará de:
* Uma conta AWS devidamente configurada no seu ambiente de trabalho
* Python 3.9
* Serverless Framework

Aqui está o passo a passo:

1. Instale as dependências do Python:
```bash
pip install -r requirements.txt
```

2. Implante na AWS:
```bash
sls deploy
```

3. Acesse o Console da AWS, vá até a seção do S3 e faça o upload das suas fotos HEIC no bucket "heic-input-*".

4. Vá até o bucket "jpg-output-*" e baixe seus arquivos convertidos.

# Resultados

Consegui converter todas as imagens da minha esposa em segundos, apenas enviando os arquivos pela interface de upload do S3 e baixando-os do bucket S3.

O custo estimado para isso é de $0,000002293 por imagem convertida.