from components.config import COLORS


def get_feature_color(name: str) -> str:
    if '_Freq_' in name:
        return COLORS['frequency']
    elif '_missing' in name:
        return COLORS['missingness']
    elif any(x in name for x in ['_Min_', '_Max_', '_Mean_', '_Std_']):
        return COLORS['window']
    return COLORS['raw']


def is_raw_feature(name: str) -> bool:
    return not any(
        x in name for x in ['_Freq_', '_missing', '_Min_', '_Max_', '_Mean_', '_Std_']
    )
