## Informações 

O limite de memória definidos nos contêiners é imposto via cgroups, e a maioria das ferramentas Linux que fornecem métricas de recursos do sistema foram criadas antes mesmo da existência de cgroups (por exemplo: free ou top). 


Eles costumam ler métricas de memória do procsistema de arquivos: `/proc/meminfo`, `/proc/vmstat`, `/proc/PID/smaps` e outros.
Isso significa que eles não têm consciência de cgroup . Eles sempre exibirão os números de memória do sistema host (máquina física ou virtual) como um todo, que é inútil para os contêineres modernos do Linux.

Esse módulo Python funciona apenas no linux, e foi criado exclusivamente para atender os usuários da [discloudbot.com](https://discloudbot.com)

As informações fornecidas pelo modulo são geradas pelo [cgroup](https://www.kernel.org/doc/Documentation/cgroup-v1/) no caminho `/sys/fs/cgroup/`


## Instalação

```
pip install discloud-status
```

## Forma de uso Python 3.6+

```python
import discloud

# retorna o uso/total de RAM
r = discloud.ram()
print(r) # 100/1024MB

# dados do uso de RAM
ur = discloud.using_ram()
print(ur) # 100MB

# dados do total de RAM disponível
tr = discloud.total_ram()
print(tr) # 1GB

```

## Possíveis Erros
Se um dos arquivos estiver vazio, ele retornará um erro como este:
`Dados não encontrados`


## LICENSE
Este projeto está licenciado sob a Licença Apache V2. Consulte [LICENSE](LICENSE) para obter mais informações.


