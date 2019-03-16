function! Rc()
python << EOF
# reverse all content in vim buffer, help to check credit card bill
import vim
cur_buf = vim.current.buffer
r_content=[cc for cc in cur_buf][::-1]
cur_buf.append('---belowed are converted content---')
for cc in r_content:
    cur_buf.append(cc)

EOF
endfunction
