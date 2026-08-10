import './HistoryList.css';




const VERDICT_LABELS = {
    low_risk: { label: 'Low', className: 'history-item-badge-low' },
    medium_risk: { label: 'Medium', className: 'history-item-badge-medium' },
    high_risk: { label: 'High', className: 'history-item-badge-high' }
}



function HistoryList({ history, isLoading, onSelect }) {
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
                        onClick={() => onSelect?.(item)}
                    >
                        <div className='history-item-main'>
                            <span className='history-item-url'>{item.url}</span>
                        </div>
                        <div className='history-item-meta'>
                            <span className='history-item-score'>{item.risk_score}/100</span>
                            <span className=''>{badge.label}</span>
                        </div>
                    </li>
                )
            })}
        </ul>
    )
}


export default HistoryList;