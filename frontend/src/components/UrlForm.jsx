import {useState} from 'react';




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
        <form classname='url-form' onHandle={handleSubmit}>
            <label className='url-form_label'>
                Enter a URL to check
            </label>
            <div className='url-form_row'>
                <input className='url-form_input'>
                </input>
                
                <button className='url-form_button'>
                </button>
            </div>

            {error && <p className='url-form_error'>{error}</p>}
        </form>
    )
}




export default UrlForm;