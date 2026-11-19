"""地形侵蚀：坡度、汇流与沉积。"""


def normalize_neighborhood(weights):
    """归一化邻域权重，总和为 1。

    边界单元只按实际存在的邻居计入，避免重复计数。
    权重全为 0 时退化为均分。
    """
    weights = list(weights)
    if not weights:
        return []
    total = sum(weights)
    if total == 0:
        share = 1.0 / len(weights)
        return [share for _ in weights]
    return [w / total for w in weights]


def rainfall_to_unit(values):
    """把 0–255 雨量映射到 0–1。

    超出范围的值先钳制到 [0, 255]，再除以 255，与汇流累积统一量纲。
    """
    result = []
    for value in values:
        clamped = min(255.0, max(0.0, value))
        result.append(clamped / 255.0)
    return result


def enforce_min_slope(profile, min_slope):
    """保证相邻高程下落不超过 min_slope。

    河道下切时，若下游比上游低出超过 min_slope，就把下游抬高到
    上游高度减去 min_slope，得到满足约束的新剖面。
    """
    profile = list(profile)
    if not profile:
        return []
    result = [profile[0]]
    for height in profile[1:]:
        lowest = result[-1] - min_slope
        result.append(height if height >= lowest else lowest)
    return result


def split_sediment(mass, fractions):
    """按粒径比例拆分沉积物总量。

    每一粒径分得 mass * fraction / sum(fractions)。比例全为 0 时
    按粒径数量均分，保证总量守恒。
    """
    fractions = list(fractions)
    if not fractions:
        return []
    total = sum(fractions)
    if total == 0:
        share = mass / len(fractions)
        return [share for _ in fractions]
    return [mass * fraction / total for fraction in fractions]


def align_tile_seam(left, right):
    """把相邻瓦片接缝高度取平均并对齐。

    左瓦片最后一个高度与右瓦片第一个高度是同一接缝，取二者平均
    后写回两侧；任一瓦片为空时保持原样。
    """
    left = list(left)
    right = list(right)
    if left and right:
        seam = (left[-1] + right[0]) / 2.0
        left[-1] = seam
        right[0] = seam
    return left, right


def recompute_normals(heights):
    """按高度差重算坡度/法线。

    返回相邻高程之间的梯度，长度比输入少 1。
    """
    heights = list(heights)
    return [heights[i + 1] - heights[i] for i in range(len(heights) - 1)]


def fill_basins(heights):
    """把内部洼地抬到邻域最低值。

    只处理内部单元（边界作为出口保持不变）；反复抬高低于两侧最低
    邻居的单元，直到不再变化，从而填平无出路盆地。
    """
    result = list(heights)
    if len(result) < 3:
        return result
    changed = True
    while changed:
        changed = False
        for i in range(1, len(result) - 1):
            lowest = min(result[i - 1], result[i + 1])
            if result[i] < lowest:
                result[i] = lowest
                changed = True
    return result


def clamp_erosion(strength, limit):
    """把侵蚀强度钳制到 [-limit, limit]。"""
    limit = abs(limit)
    return max(-limit, min(limit, strength))


def cache_is_fresh(cache_version, source_version):
    """缓存版本与源数据版本一致才算有效。"""
    return cache_version == source_version


def commit_tiles(statuses):
    """批量瓦片全部成功才提交。"""
    return all(statuses)
