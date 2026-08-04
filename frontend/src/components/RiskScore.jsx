import './RiskScore.css';




const VERDICT_CONFIG = {
    low_risk: { label: 'Low Risk', className: 'risk-score-low' },
    medium_risk: { label: 'Medium Risk', className: 'risk-score-medium' },
    high_risk: { label: 'High Risk', className: 'risk-score-high' }
};



function RiskScore({ score, verdict }) {
    const config = VERDICT_CONFIG[verdict] ?? VERDICT_CONFIG.low_risk;

    return (
        <div className={`risk-score ${config.className}`}> 
            <div className='risk-score-circle'>
                <span className='risk-score-number'>{score}</span>
                <span className='risk-score-max'>/100</span>
            </div>
            <span className='risk-score-label'>{config.label}</span>
        </div>
    )
}




export default RiskScore;