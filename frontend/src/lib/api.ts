import axios,{ AxiosError, AxiosRequestConfig } from 'axios';
const API_URL=process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
const api=axios.create({
    baseURL:`${API_URL}/api`,
    headers:{
        'Content-Type':'application/json',

    },

});
api.interceptors.request.use((config)=> {
    if (typeof window!=='undefined'){
        const token=localStorage.getItem('token');
        if (token){
            config.headers.Authorization='Bearer ${token}';
        }
    }
    return config;
});
api.interceptors.response.use(
    (response)=>response,
    async(error:AxiosError)=>{
        const originalRequest=error.config as AxiosRequestConfig & { _retry?: boolean };
        if (error.response ?.status===401 && !originalRequest._retry){
            originalRequest._retry=true;
            if (typeof window !=='undefined'){
                const refreshToken =localStorage.getItem('refresh_token');
                if (refreshToken){
                    try{
                        const {data }=await axios.post(`${API_URL}/api/token/refresh/`,{
                            refresh:refreshToken,
                        });
                        localStorage.setItem(`access_token`,data.access);
                        if (!originalRequest.headers) {
                            originalRequest.headers = {};
                        }
                        originalRequest.headers.Authorization=`Bearer ${data.access}`;
                        return api(originalRequest);
                      }  catch{
                         localStorage.removeItem('access_token');
                         localStorage.removeItem('refresh_token');
                         window.location.href='/auth/login';
                        }
                    }
                }
            }
            return Promise.reject(error);
        }
    
);
export default api;