"""地形侵蚀：坡度、汇流与沉积：待实现的核心模块。"""


def normalize_neighborhood(weights):
    """归一化邻域权重，总和为 1。"""
    raise NotImplementedError

def rainfall_to_unit(values):
    """把 0–255 雨量映射到 0–1。"""
    raise NotImplementedError

def enforce_min_slope(profile, min_slope):
    """保证相邻高程下落不超过 min_slope。"""
    raise NotImplementedError

def split_sediment(mass, fractions):
    """按粒径比例拆分沉积物总量。"""
    raise NotImplementedError

def align_tile_seam(left, right):
    """把相邻瓦片接缝高度取平均并对齐。"""
    raise NotImplementedError

def recompute_normals(heights):
    """按高度差重算坡度/法线。"""
    raise NotImplementedError

def fill_basins(heights):
    """把内部洼地抬到邻域最低值。"""
    raise NotImplementedError

def clamp_erosion(strength, limit):
    """把侵蚀强度钳制到 [-limit, limit]。"""
    raise NotImplementedError

def cache_is_fresh(cache_version, source_version):
    """缓存版本与源数据版本一致才算有效。"""
    raise NotImplementedError

def commit_tiles(statuses):
    """批量瓦片全部成功才提交。"""
    raise NotImplementedError
