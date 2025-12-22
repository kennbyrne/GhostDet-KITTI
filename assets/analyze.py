import pandas as pd

df = pd.read_csv('runs/detect/ghostdet_local2/results.csv')

print('\nEpoch | mAP@0.5 | Recall')
print('------------------------')
for _, row in df.iterrows():
    epoch = int(row['epoch'])
    mAP50 = row['metrics/mAP50(B)']
    recall = row['metrics/recall(B)']
    print(f'{epoch:>5} | {mAP50:.4f} | {recall:.4f}')

# Future work: Save clean CSV for MATLAB/Excel
df[['epoch', 'metrics/mAP50(B)', 'metrics/recall(B)']].rename(columns={
    'metrics/mAP50(B)': 'mAP_0.5',
    'metrics/recall(B)': 'recall'
}).to_csv('val_metrics.csv', index=False)

print('\n Saved val_metrics.csv')