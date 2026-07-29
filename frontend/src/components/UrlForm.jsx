import {useState} from 'react';
import './UrlForm.css';




function UrlForm({ onSubmit, isLoading }) {
    const [url, setUrl] = useState('');
    const [error, setError] = useState('');


    const handleSubmit = (e) => {
        e.preventDefault();
        setError('');

        if (!url.trim()) {
            setError('Please enter a URL to be analyzed.');
            return;
        }

        onSubmit(url.trim());
    }


    return (
        <form className='url-form' onSubmit={handleSubmit}>
            <label className='url-form_label'>
                Enter a URL to check
            </label>
            <div className='url-form_row'>
                <input 
                    id='url-input'
                    className='url-form_input'
                    type='text'
                    placeholder='http://example.com/login'
                    value={url}
                    onChange={(e) => setUrl(e.target.value)}
                    disabled={isLoading}
                />
                <button className='url-form_button' type='submit' disabled={isLoading}>
                    {isLoading? 'Analyzing...' : 'Analyze'}
                </button>
            </div>

            {error && <p className='url-form_error'>{error}</p>}
        </form>
    )
}




export default UrlForm;