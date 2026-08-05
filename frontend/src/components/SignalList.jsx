import './SignalList.css';




const SIGNAL_LABELS = {
    suspicious_tld: 'Suspicious Domain Extension',
    ip_based_url: 'IP-Based URL',
    typosquatting: 'Brand Impersonation',
    url_shortner: 'Link Shortener'
};



function SignalList({ signals }) {
    return (
        <ul className='signal-list'>
            {signals.map((signal) => (
                <li key={signal.name} className={`signal-list-item ${
                    signal.flagged ? 'signal-list-item-flagged' : 'signal-list-item-cleared'
                }`}
                >
                    <span className='signal-list-icon'>{signal.flagged ? 'FLAGGED' : 'OK'}</span>
                    <div className='signal-list-content'>
                        <span className='signal-list-name'>
                            {SIGNAL_LABELS[signal.name] ?? signal.name}
                        </span>
                        <span className='signal-list-detail'>{signal.detail}</span>
                    </div>
                </li>
            ))}
        </ul>
    )
}




export default SignalList