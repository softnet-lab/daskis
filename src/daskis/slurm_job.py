"""
SLURM related functionalities, that can be used from inside a SLURM job
"""

__slurm_env_map = {
    # job id
    'SLURM_JOB_ID': 'job_id',  # alias SLURM_JOBID
    'SLURM_SUBMIT_DIR': 'submit_dir',
    'SLURM_SUBMIT_HOST': 'submit_host',  # se01.grid.tuc.gr
    'SLURM_JOB_NAME': 'job_name',
    'SLURM_CLUSTER_NAME': 'cluster_name',

    # job user and user id
    'SLURM_JOB_USER': 'job_user',
    'SLURM_JOB_UID': 'job_uid',
    'SLURM_JOB_GID': 'job_gid',

    # job resource alloc
    'SLURM_JOB_QOS': 'job_qos',
    'SLURM_JOB_CPUS_PER_NODE': 'cpus_per_node',
    # SLURM_CPUS_ON_NODE=4  deprecated
    'SLURM_TASKS_PER_NODE': 'tasks_per_node',
    'SLURM_MEM_PER_NODE': 'mem_per_node',
    'SLURM_JOB_NUM_NODES': 'job_num_nodes',
    'SLURM_JOB_NODELIST': 'nodelist',
    # SLURM_NODE_ALIASES=(null)
    'SLURM_JOB_PARTITION': 'partition',  # queue name (aTUc, compute, gpu etc)

    # actual allocation
    'SLURM_NNODES': 'num_nodes',
    'SLURM_NTASKS': 'num_tasks',
    'SLURM_NPROCS': 'num_procs',

    # location
    'SLURM_NODEID': 'node_id',
    'SLURMD_NODENAME': 'node_name',
    'SLURM_LOCALID': 'local_id',
    'SLURM_TASK_PID': 'task_pid',

    'SLURM_PROCID': 'proc_id',  # MPI rank

    # topology
    'SLURM_TOPOLOGY_ADDR': 'topology_addr',
    'SLURM_TOPOLOGY_ADDR_PATTERN': 'topology_addr_pattern',


    'foo':
    '''
    SLURM_GTIDS=0
    SLURM_WORKING_CLUSTER=tuc:se01:6817:8704:101
    SLURM_NODELIST=wn[005-008]
    SLURM_PRIO_PROCESS=0
    '''
}


class Context:
    """Represents the running SLURM job and is accessible from within the job."""

    def __init__(self, environ=None):
        # slurm variables
        if environ is None:
            import os
            self.environ = os.environ
        else:
            self.environ = environ

    def under_slurm(self):
        """Returns True if running under SLURM, else returns false"""
        return 'SLURM_JOB_ID' in self.environ

    def __cached(self, name, env_name):
        try:
            return getattr(self, name)
        except AttributeError:
            v = self.environ[env_name]
            setattr(self, name, v)
            return v

    def __cached_convert(self, name, env_name, convert):
        try:
            return getattr(self, name)
        except AttributeError:
            v = self.environ[env_name]
            v = convert(v)
            setattr(self, name, v)
            return v

    def __cached_opt(self, name, env_name, default_val=None):
        try:
            return getattr(self, name)
        except AttributeError:
            v = self.environ.get(env_name, default_val)
            setattr(self, name, v)
            return v

    def __cached_opt_convert(self, name, env_name, convert, default_val=None):
        try:
            return getattr(self, name)
        except AttributeError:
            if env_name in self.environ:
                v = convert(self.environ[env_name])
            else:
                v = default_val
            setattr(self, name, v)
            return v

    @property
    def job_id(self):
        return self.__cached('_cached_job_id', 'SLURM_JOB_ID', int)

    @property
    def job_name(self):
        return self.__cached('_cached_job_name', 'SLURM_JOB_NAME')

    @property
    def submit_dir(self):
        return self.__cached('_cached_submit_dir', 'SLURM_SUBMIT_DIR')

    @property
    def submit_host(self):
        return self.__cached('_cached_submit_host', 'SLURM_SUBMIT_HOST')

    @property
    def cluster(self):
        return self.__cached('_cached_cluster', 'SLURM_CLUSTER_NAME')

    @property
    def num_nodes(self):
        return self.__cached('_cached_num_nodes', 'SLURM_JOB_NUM_NODES')

    @property
    def node_id(self):
        return self.__cached('_cached_node_id', 'SLURM_NODEID')

    @property
    def node_name(self):
        return self.__cached('_cached_node_name', 'SLURMD_NODENAME')

    @property
    def task_pid(self):
        return self.__cached('_cached_task_pid', 'SLURM_TASK_PID')

    @property
    def task_id(self):
        return self.__cached('_cached_task_id', 'SLURM_LOCALID')

    @property
    def num_tasks(self):
        return self.__cached('_cached_num_tasks', 'SLURM_NTASKS')

    @property
    def proc_id(self):
        return self.__cached('_cached_proc_id', 'SLURM_PROCID')

    @property
    def num_procs(self):
        return self.__cached('_cached_num_procs', 'SLURM_NPROCS')

    @property
    def partition(self):
        return self.__cached('_cached_partition', 'SLURM_JOB_PARTITION')

    @property
    def account(self):
        return self.__cached_opt('_cached_partition', 'SLURM_JOB_PARTITION')
