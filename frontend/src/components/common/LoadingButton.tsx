import { Button, CircularProgress, ButtonProps } from '@mui/material'

interface LoadingButtonProps extends ButtonProps {
  loading: boolean
}

export default function LoadingButton({ loading, children, disabled, ...rest }: LoadingButtonProps) {
  return (
    <Button disabled={loading || disabled} {...rest}>
      {loading && <CircularProgress size={20} sx={{ mr: 1 }} />}
      {children}
    </Button>
  )
}