import './HistoryList.css';




const VERDICT_LABELS = {
    low_risk: { label: 'Low', className: 'history-item-badge-low' },
    medium_risk: { label: 'Medium', className: 'history-item-badge-medium' },
    high_risk: { label: 'High', className: 'history-item-badge-high' }
}


function formatTimestamp(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
        month: 'short',
        day: 'numeric',
        hour: 'numeric',
        minute: '2-digit'
    });
}



function HistoryList({ history, isLoading, onSelect, onDelete }) {
    if (isLoading) {
        return (
            <p className='history-list-status'>
                Loading history...
            </p>
        )
    }

    if (!history || history.length === 0) {
        return (
            <p className='history-list-status'>
                No scans yet.  Analyze a URL to update this list.
            </p>
        )
    }


    return (
        <ul className='history-list'>
            {history.map((item) => {
                const badge = VERDICT_LABELS[item.verdict] ?? VERDICT_LABELS.low_risk;

                return (
                    <li
                        key={item.id}
                        className='history-item'
                    >
                        <div className='history-item-clickable' onClick={() => onSelect?.(item)}>
                            <div className='history-item-main'>
                                <span className='history-item-url'>{item.url}</span>
                                <span>{formatTimestamp(item.scanned_at)}</span>
                            </div>
                            <div className='history-item-meta'>
                                <span className='history-item-score'>{item.risk_score}/100</span>
                                <span className={`history-item-badge ${badge.className}`}>{badge.label}</span>
                            </div>
                        </div>
                        
                        <button
                            type='button'
                            className='history-item-delete'
                            aria-label={`Delete scan of ${item.url}`}
                            onClick={(e) => {
                                e.stopPropagation();
                                onDelete?.(item.id);
                            }}
                        >
                            X
                        </button>
                    </li>
                );

            })}
        </ul>
    )
}




export default HistoryList;