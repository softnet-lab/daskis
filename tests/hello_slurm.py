import daskis.slurm_job as sj

ctx = sj.Context()

if not ctx.under_slurm():
    print("This script must be run inside a SLURM job")
    raise RuntimeError("Cannot execute unles under SLURM")

print("Hello SLURM world!")
print("Job id           :", ctx.job_id)
print("Job name:        :", ctx.job_name)

print("Node  id :        :", ctx.node_id)
print("Node name:        :", ctx.node_name)

print("Task pid :        :", ctx.task_pid)
print("Task  id :        :", ctx.task_id)
print("Tasks    :        :", ctx.num_tasks)

print("Proc  id :        :", ctx.proc_id)
print("Nproc    :        :", ctx.num_procs)
