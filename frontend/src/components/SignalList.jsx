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
                <li className='signal-item'>
                    {signal.name}
                </li>
            ))}
        </ul>
    )
}




export default SignalList