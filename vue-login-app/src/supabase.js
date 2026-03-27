import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'https://jfzjurszphfgdlyekblz.supabase.co'
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'sb_publishable_7smNvHE9eGJEfF_EwyVg6g_NOkf_XHj'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
