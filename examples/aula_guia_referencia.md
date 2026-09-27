# Entrar no e-mail da empresa com chave de acesso, sem digitar senha

Troque a senha do e-mail da empresa por uma chave de acesso e entre com a digital ou o rosto.

Com a chave de acesso ligada, você entra no e-mail da empresa com a digital, o rosto ou o PIN
do celular, e a página falsa que pede a sua senha perde a utilidade, porque não existe senha
para entregar. A troca pede o celular que você já usa e cabe numa pausa do expediente.

Adiar tem prazo. A Microsoft passou a oferecer a chave de acesso como forma padrão de entrar
nas contas corporativas que ela administra a partir de 1º de setembro de 2026 e vai desligar o
envio de código por SMS e por ligação nessas contas em 1º de fevereiro de 2027 (Microsoft,
julho de 2026). Se a sua empresa usa essas contas, a troca vem de qualquer jeito; fazer agora
deixa a escolha da hora com você.

## Por que a chave de acesso resiste ao golpe da página falsa

A chave de acesso (em inglês, passkey: um par de chaves em que a parte secreta nunca sai do seu
aparelho) funciona como uma fechadura que só abre com a chave que fica no seu bolso. O serviço
de e-mail guarda só a parte pública; na hora de entrar, o seu aparelho prova que tem a parte
secreta, e você destrava essa prova com a digital, o rosto ou o PIN. O padrão que sustenta
isso é o WebAuthn, recomendação do W3C de março de 2019, e ele amarra cada chave ao endereço
do serviço: uma página falsa, em outro endereço, não recebe nada que sirva para entrar.

A troca já é comum. Numa pesquisa de abril de 2026 com 11 mil consumidores de dez países, sem o
Brasil na amostra, 75% disseram ter ligado a chave de acesso em ao menos uma conta, e 68% das
1,4 mil empresas ouvidas já adotavam ou estavam adotando a chave no login dos funcionários
(FIDO Alliance, maio de 2026). Para a sua empresa, o número importa menos que o mecanismo: a
senha que não existe não vaza.

## Como ligar a chave de acesso nas contas da empresa

Antes de começar, ligue o bloqueio de tela do celular (digital, rosto ou PIN) e tenha à mão a
senha atual do e-mail, que o serviço pede uma última vez para confirmar que a conta é sua.

1. Abra as configurações de segurança da conta de e-mail no computador e procure a opção de
   chave de acesso. Deu certo quando aparece o botão para criar uma chave; se a opção não
   aparecer, quem administra as contas da empresa ainda não liberou o recurso, e o conserto é
   pedir a liberação antes de seguir.
2. Crie a chave e confirme com a digital, o rosto ou o PIN quando o celular pedir. Você vê a
   chave nova na lista, com o nome do aparelho. O erro mais comum é confirmar no celular de
   outra pessoa da equipe; se isso acontecer, apague essa chave da lista e crie de novo no seu.
3. Crie uma segunda chave em outro aparelho seu, como o computador do escritório. Confira se a
   lista mostra os dois aparelhos: sem o segundo, perder o celular vira pedido de recuperação
   da conta, justamente o caminho que atacantes tentam sequestrar se passando pelo dono
   (Microsoft, maio de 2026).
4. Saia da conta e entre de novo escolhendo a chave de acesso. Funcionou quando o e-mail abre
   sem pedir senha.
5. Apague as perguntas de segurança da recuperação, se a conta ainda usa, e deixe os dois
   aparelhos como forma de recuperar o acesso. Deu certo quando a página de recuperação lista
   os aparelhos e nenhuma pergunta. A Microsoft tira essas perguntas das contas corporativas
   em janeiro de 2027, por serem fáceis de adivinhar ou de arrancar numa conversa (Microsoft,
   maio de 2026).

Se a equipe divide um e-mail, como o do atendimento, crie uma chave no aparelho de cada pessoa
que atende e apague a chave de quem sair da empresa no mesmo dia da saída. Se o seu serviço de
e-mail ainda não oferece chave de acesso, ligue a verificação em duas etapas por aplicativo,
sem SMS, e confira de novo no começo do próximo trimestre.

Suponha uma papelaria com três pessoas e dois e-mails, o do dono e o do atendimento. São três
aparelhos no e-mail do atendimento e dois no do dono: cinco chaves, criadas numa manhã, na
ordem dos passos acima. No dia em que alguém do caixa sair, o dono apaga uma chave, e o e-mail
do atendimento continua abrindo nos outros dois aparelhos.

Está pronto quando você entra nas contas da empresa sem digitar senha e a lista de cada uma
mostra ao menos dois aparelhos seus. Anote hoje quais contas ainda pedem senha: na próxima
aula, essa lista decide a ordem da troca.

## Fontes

- FIDO Alliance, State of Passkeys 2026, 7 de maio de 2026. https://fidoalliance.org/fido-alliance-reports-accelerating-global-passkey-adoption-on-world-passkey-day-2026/
- Microsoft, Passkeys are the default authentication method in Entra ID, 13 de julho de 2026. https://www.microsoft.com/en-us/security/blog/2026/07/13/microsoft-entra-id-security-updates-passkeys-are-the-default-authentication-method-in-entra-id/
- Microsoft, World Passkey Day: advancing passwordless authentication, 7 de maio de 2026. https://www.microsoft.com/en-us/security/blog/2026/05/07/world-passkey-day-advancing-passwordless-authentication/
- W3C, Web Authentication Level 1, 4 de março de 2019 (origem do conceito). https://www.w3.org/TR/2019/REC-webauthn-1-20190304/
